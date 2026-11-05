## orchid-examples

**What it is.** Five runnable examples behind the ORCHID paper (Cu–Zr MLIP→CALPHAD tuning, ESPEI MCMC negative result,
one-shot MLIP phase-diagram scoring, MLIP formation-enthalpy benchmark, Parquet quickstart notebook). Each has a cached
"quick path" that rebuilds figures and tables, checked byte-for-byte by `tests/check_quick_paths.py`.

**Commands** (work copy `cp -a` of the shallow clone to `/tmp/arroyave/work/orchid-examples`; CPython 3.12.3 from the
runner (quickstart pins 3.12.14); every install and run through `/tmp/sbx/clean`, `OMP_NUM_THREADS=1`):

```sh
uv venv --python 3.12 /tmp/arroyave/venvs/orchid-examples              # union of the 4 small examples' requirements.txt
uv pip install --python /tmp/arroyave/venvs/orchid-examples/bin/python numpy==2.3.2 scipy==1.16.1 matplotlib==3.10.7
uv venv --python 3.12 /tmp/arroyave/venvs/orchid-examples-quickstart    # quickstart/requirements.txt (exact pins)
uv pip install --python .../orchid-examples-quickstart/bin/python -r quickstart/requirements.txt
uv venv --python 3.12 /tmp/arroyave/venvs/orchid-examples-full          # oneshot-benchmark/requirements-full.txt (pycalphad 0.11.2)
uv pip install --python .../orchid-examples-full/bin/python -r oneshot-benchmark/requirements-full.txt
export ORCHID_DATA=/tmp/arroyave/src/orchid-calphad__orchid-data
python tests/check_quick_paths.py cuzr-phaseforgeplus --keep                                  # strict sha256 (default)
python tests/check_quick_paths.py cuzr-espei-mcmc oneshot-benchmark mlip-formation-enthalpy --keep
.../orchid-examples-quickstart/bin/python tests/check_quick_paths.py quickstart --keep
python tests/check_quick_paths.py <each example> --pixel-tol 2.0                             # CI setting, all 5 re-run
python tests/check_hygiene.py
python scripts/orchid_examples_png_rms.py /tmp/arroyave/work/orchid-examples                  # diagnose the diffs
```

All three installs resolved from the pins on Linux with no errors (including the macOS-only `appnope`, a pure wheel).

**Quick paths** (logs `logs/orchid-examples-quick-*.log`; diff diagnosis `logs/orchid-examples-quick-diffs.log`):

| example | time here (README / examples.json) | byte-identical | differing | verdict |
|---|---|---|---|---|
| cuzr-phaseforgeplus | 383 s cold, 28 s warm (~4 min / 6 min) | `gate.json`, both PDFs | 2 PNGs: pixel RMS 0.010, 0.009 (of 255) | PASS with CI tolerance (re-run: exit 0); FAIL strict |
| cuzr-espei-mcmc | 20 s (~1 min / 2 min) | `gate_sgte_start.json`, PDF | PNG: pixel RMS 0.000 | PASS with CI tolerance (re-run: exit 0) |
| oneshot-benchmark | 139 s, 131 s ("about 30 s" / 2 min) | PDF | PNG RMS 0.011; `grace_grid_score.json` (one field, see bug 1) | PASS with CI tolerance (re-run: exit 0, JSON diff only a "warn") |
| mlip-formation-enthalpy | 21 s (~1 min / 2 min) | `summary.json` | PNG RMS 0.000; PDF bytes (see below) | PASS with CI tolerance (re-run: exit 0, PDF "warn") |
| quickstart (full release via `ORCHID_DATA`) | 9 s (~20 s / 2 min) | PDF | PNG RMS 0.000 | PASS with CI tolerance (re-run: exit 0) |

`check_hygiene.py`: `430 files, 13.3 MB` / `hygiene ok` (exit 0).

Every scientific output reproduces exactly: 3 of the 4 JSON outputs (both gate tables, the MLIP saturation statistics)
are byte-identical, the fourth (grid score) differs only in an input-file hash (bug 1), and 5 of the 6 PDFs are byte-identical. With the strict default (`--pixel-tol 0`) every example exits 1
(`FAILED: cuzr-espei-mcmc, mlip-formation-enthalpy, oneshot-benchmark`, `FAILED: cuzr-phaseforgeplus`,
`FAILED: quickstart`), only because the PNG bytes differ. The regenerated PNGs are 7–21 % larger than the committed ones
for the same pixels (RMS 0.000–0.011), which points to a different PNG encoder build (here the Pillow 13.0.0 wheel,
zlib 1.3), not to a different figure. The `mlip_benchmark.pdf` difference is also compression-only: all 27 PDF streams are identical after
zlib decompression. The timings are inflated by CPU sharing with four other agents on 4 vCPUs.

**Full path (≤15 min on CPU).** The one-shot scorer (`oneshot-benchmark/scripts/score.py`, pycalphad 0.11.2) rescoring the
shipped TDBs against ORCHID evidence (log `logs/orchid-examples-full-oneshot-{sgte,grace}.log`, summary
`data/orchid-examples-oneshot-rescore.json`, headline table `data/orchid-examples-headlines.csv`):

| model | README | reproduced | per-point predictions vs committed | wall |
|---|---|---|---|---|
| SGTE CuZr-94Zen-LB | 0.72 [0.59, 0.84] / 0.73 [0.70, 0.76] | **0.722 [0.593, 0.843] / 0.728 [0.696, 0.761]** | 315/315 identical | 31 s (11 s scoring) |
| GRACE-2L-OMAT, MLIP-only (Spark build TDB) | 0.426 / 0.410 | **0.426 [0.296, 0.554] / 0.410 [0.383, 0.435]** | 315/315 vs `results/mlips/`; 305/315 vs the Studio build (README: "10 of 315 differ") | 29 s |

(field / boundary prevalence-weighted recall, 95 % bootstrap CI; 0 failed equilibrium cells.) The "tuned 9/13
invariants" headline comes from `cuzr-phaseforgeplus/cached/gate.json`, which regenerated byte-identically:
`gate_counts {'SGTE': [12, 13], 'MLIP-only': [0, 13], 'tuned': [9, 13]}`.

**Al–Cu / Cu–Ni scoring is not possible with the shipped scorer.** It is hard-wired to Cu–Zr: `COMPS = ["CU", "ZR", "VA"]`
(score.py line 39), conditions on `v.X("ZR")`, evidence points carry `x_Zr`, and the benchmark phase classes and
`build_evidence.py` are Cu–Zr-only. Porting it needs new evidence and a phase-class map. ORCHID's Al–Cu ESPEI data are
thin for that (3 ZPF datasets for AlCu-21Kro, see below).

**Quickstart notebook re-run for Al–Cu, Al–Si, Al–Zr** (full release). `scripts/orchid_examples_quickstart_system.py`
copies the notebook, substitutes `SYSTEM` and the export TDB name, and executes it with nbclient (~4 s each; logs
`logs/orchid-examples-full-quickstart-{AL-CU,AL-SI,AL-ZR}.log`):

| system (export TDB) | values in release | accepted multi-reader experimental | ΔHf among them | DFT parity rows (default subset) | ESPEI export → `load_datasets` |
|---|---|---|---|---|---|
| AL-CU (AlCu-21Kro) | 114 (83 invariant T, 22 phase composition, 9 transition T) | 40 | 0 | 0 | 3 ZPF datasets (1 experimental, 2 invariants) → 3 loaded |
| AL-SI (none exists) | 13 (9 invariant T, 4 transition T) | 0 | 0 | 0 | no Al–Si ESPEI datasets in `espei/index.csv` → 0 |
| AL-ZR (AlZr-01Wan) | 743 | 170 | 58 | MP 45: mean residual 3.59, median 2.06, sd 7.09; OQMD 45: 3.52 / 1.92 / 7.14 kJ/mol-atom | 12 HM_FORM datasets → 12 loaded |

**Problems found**
1. *Stale hash in a committed output.* `oneshot-benchmark/figures/grace_grid_score.json` differs only in
   `grid_sha256`: committed `1ef9f5974c94…` equals the SHA-256 of `grace_grid.csv` with **CRLF** line endings, while
   the shipped `npz_to_grid.py` (`open(..., "w", newline="")`, `lineterminator="\n"`) writes LF on every platform
   (`b3497bdc8902…`). The scores are identical. This points to a committed output made by an earlier script version
   (the csv module's default terminator is `\r\n`) and not regenerated, so `check_quick_paths.py --strict` fails for
   oneshot-benchmark on any OS.
2. *Strict default can't pass off the authors' platform.* `check_quick_paths.py` without `--pixel-tol` fails all five
   examples on PNG bytes alone; only the CI setting (`--pixel-tol 2.0`) passes. The README's "regenerates
   byte-identically" holds for the JSON and PDF outputs, not the PNGs.
3. *Quickstart is Cu–Zr-only in code.* `SYSTEM = "CU-ZR"` and the `CuZr-94Zen-LB` export name are hard-coded. For
   other systems the printed label stays "Cu-Zr values", and the figure keeps the title "Cu–Zr: literature vs DFT
   formation enthalpies" and fixed axes −30…2 kJ/mol-atom. For Al–Zr (ΔHf down to −71 kJ/mol-atom) nearly every point
   falls off the axes, so I discarded that figure.
4. *Data caveat visible through the quickstart filters.* Among Al–Zr "accepted, experimental, multi_reader" ΔHf values,
   several carry `unit = "unknown"` (e.g. Al3Zr2 −55.0, Al2Zr −54.0, AlZr −53.0). The quickstart filter does not
   screen on unit.
5. *Timing claims are optimistic under load.* The oneshot quick path took 139 s and 131 s against "about 30 s" (figure plus
   2,000-sample bootstraps on one shared core).
6. *Quick paths write into the example tree.* `cuzr-phaseforgeplus/scripts/fig_overlay.py` caches the phase-diagram geometry
   as `cuzr-phaseforgeplus/work/pdgeo_{SGTE,MLIP-only,tuned}_*.json` (840 KB) inside the checkout, not in the OUT dir
   that `check_quick_paths.py` passes, so only the first run is cold (383 s; the second took 28 s). The quickstart also
   writes `quickstart/export/`. Both paths are git-ignored, so nothing is dirtied, but a timing or regeneration check
   on a used checkout reuses the cache.

| orchid-examples | OK (3 uv venvs, py3.12.3; all pins resolve on Linux) | 5 quick paths (strict + CI tolerance), hygiene, full-path rescoring of SGTE and GRACE Cu–Zr TDBs, quickstart re-run for Al–Cu/Al–Si/Al–Zr | PASS (CI tolerance) / strict sha256 FAIL on PNG bytes only | 3/4 JSON + 5/6 PDFs byte-identical (4th JSON differs only in a file hash); SGTE 0.722/0.728 and GRACE 0.426/0.410 reproduced with 315/315 identical predictions; scorer is Cu–Zr-only; committed grid hash is stale (CRLF) |
