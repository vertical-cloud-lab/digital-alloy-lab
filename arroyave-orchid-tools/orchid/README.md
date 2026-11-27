# ORCHID group (github.com/orchid-calphad): install and test runs

Issue #235. Run on 2026-11-05 (UTC) on a shared GitHub Actions runner: 4 vCPU, 15 GB RAM shared with four other agents,
no GPU, Ubuntu, CPython 3.12.3 (3.13 where a repo's CI pins it), uv for every environment. Every install and
third-party script ran through the scrubbed-environment wrapper `/tmp/sbx/clean` with `OMP_NUM_THREADS=1`. The repos
are shallow clones under `/tmp/arroyave/src/orchid-calphad__*`. orchid-data and orchid-project.org were treated as
read-only, so anything that writes ran on a copy under `/tmp/arroyave/work/`. No paid API calls, no publishing, no
git writes.

**Bottom line.** Every repo installs from what it ships (orchid-bench and orchid-project.org have no dependency manifest;
their READMEs' package lists work unpinned) and their shipped tests and checks pass. Every headline number we re-ran reproduces:

| claim | reproduced |
|---|---|
| SGTE Cu–Zr one-shot recall 0.72 / 0.73 | 0.722 / 0.728, 315/315 identical predictions |
| GRACE MLIP-only 0.426 / 0.410 | 0.426 / 0.410 |
| tuned 9/13 invariants (MLIP-only 0/13, SGTE 12/13) | gate table byte-identical |
| orchid-bench extractor scores | 19/19 extractors rescored identically (to 1e-16) |

The byte-identical checks fail only on PNG encoding and on one stale committed hash.

**What matters for our Al/Cu work:**
- **Al–Si:** ORCHID has 13 values and **none accepted**, with no ESPEI datasets, so `get_invariant_reactions(source="literature")` returns no data.
- **Al–Cu:** thin. There are 114 values from 4 papers, 30 accepted experimental invariants, no formation enthalpies, no DFT parity rows and 3 ZPF datasets for AlCu-21Kro. The θ eutectic is never matched to literature because of a phase-label parsing gap.
- **Al–Zr:** the best-covered Al system, with 743 values, 88 accepted experimental invariants, 58 accepted multi-reader ΔHf values and 210 ESPEI datasets.
- **Cu–Ni:** no accepted invariants.
- **Ternaries:** no data for Cu–Al–Ni–Fe (nickel aluminium bronze) or Al–Mn–Cr–Zr.
- **Scorer:** the one-shot phase-diagram scorer is hard-wired to Cu–Zr, so it cannot score an Al–Cu or Cu–Ni TDB without porting.

Per-system counts are in `data/al-cu-coverage.csv`. The experimental invariants for reuse are in `data/al-cu-literature-invariants.csv` (345 rows; T in K and °C, compositions as mole fractions, DOI per row).

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

## orchid-mcp

**What it is.** An MCP server (15 tools, 4 resources, 1 prompt) over the ORCHID data release. It serves literature
values with provenance, the calculated SGTE binary diagrams, Materials Project and OQMD hulls, and the TDB catalogue.
It runs either on the official `mcp` SDK (pinned `mcp==2.3.0`) or on a stdlib-only built-in JSON-RPC stdio loop.
Commit tested: `f3a4743` (2026-11-02). Local data: orchid-data `c4ebfb6` (2026-10-30) and orchid-project.org
`786f64f` (2026-11-01). Both were read-only. The tests ran from a copy at `/tmp/arroyave/work/orchid-mcp`.

**Outcome: PASS.** Both installs worked. The full test suite passed in both venvs, with and without local data. The
stdio server ran offline on both back ends (SDK and fallback) and answered every requested tool for Al–Cu, Al–Si,
Al–Mg, Al–Zr and Cu–Ni. The two back ends returned byte-identical payloads for all 40 non-error tool calls. No tool
crashed. The only errors were the ones I provoked on purpose, plus the "no data" errors listed under the findings.

### Commands
```bash
U=/home/runner/.local/bin/uv; V=/tmp/arroyave/venvs; W=/tmp/arroyave/work/orchid-mcp
D=/tmp/arroyave/src/orchid-calphad__orchid-data; S=/tmp/arroyave/src/orchid-calphad__orchid-project.org/data
cp -a /tmp/arroyave/src/orchid-calphad__orchid-mcp $W
/tmp/sbx/clean $U venv --python 3.12 $V/orchid-mcp-plain && /tmp/sbx/clean $U venv --python 3.12 $V/orchid-mcp-mcp
/tmp/sbx/clean $U pip install --python $V/orchid-mcp-plain/bin/python -e "$W[test]"       # 7 pkgs, 0.6 s
/tmp/sbx/clean $U pip install --python $V/orchid-mcp-mcp/bin/python   -e "$W[mcp,test]"   # 35 pkgs (mcp 2.3.0), 0.8 s
# tests, CI mode (no data) and with local data, in each venv
/tmp/sbx/clean bash -c "cd $W && $V/orchid-mcp-<v>/bin/python -m pytest -q -p no:cacheprovider -rs"
/tmp/sbx/clean env ORCHID_TEST_DATA_DIR=$D ORCHID_TEST_SITE_DATA_DIR=$S bash -c "cd $W && $V/orchid-mcp-<v>/bin/python -m pytest -q -p no:cacheprovider -rs --durations=10"
# JSON-RPC driver: starts `orchid-mcp` with ORCHID_DATA_DIR=$D ORCHID_SITE_DATA_DIR=$S ORCHID_OFFLINE=1
/tmp/sbx/clean $V/orchid-mcp-mcp/bin/python -I scripts/orchid_mcp_drive.py --server "$V/orchid-mcp-mcp/bin/orchid-mcp" \
   --label sdk --data-dir $D --site-dir $S --cache-dir /tmp/arroyave/work/orchid-mcp-cache --out data --log logs/orchid-mcp-stdio-sdk.log --save-trimmed
/tmp/sbx/clean $V/orchid-mcp-plain/bin/python -I scripts/orchid_mcp_drive.py --server "$V/orchid-mcp-plain/bin/orchid-mcp" --label fallback ...
/tmp/sbx/clean $V/orchid-mcp-mcp/bin/python -I scripts/orchid_mcp_probe.py ...          # accepted-vs-all and SGTE-vs-literature follow-ups
/tmp/sbx/clean $V/orchid-mcp-<v>/bin/python -I scripts/orchid_mcp_readme_sizes.py ...    # re-measures the README's CU-ZR size table
```
The driver sends `initialize`, then `notifications/initialized`, `tools/list` and 41 `tools/call` requests, each with
a 120 s timeout. For each of the 5 systems it calls `get_invariant_reactions` (`source="both"`, `limit=200`),
`get_phase_diagram` once with no point and once at 1 or 2 (x, T) points, `list_tdb_files` (pair, then `exact`) and
`compare_to_dft`. It then calls `get_formation_enthalpy` for Al2Cu, Al3Zr and Al3Mg2, plus `list_tdb_files`,
`search_systems([Al])` and `search_systems([Cu])`, and one call with a deliberately bad assessment name.

### Tests and timings
| venv | pytest, no data (CI mode) | pytest, with local data |
|---|---|---|
| plain (stdlib fallback) | 28 passed, 24 skipped, 1.4 s | 51 passed, 1 skipped (`mcp SDK not installed`), 4.3 s |
| `[mcp]` (mcp 2.3.0) | 28 passed, 24 skipped, 1.5 s | **52 passed**, 5.9 s |

Server timings over stdio:
- **Startup (`initialize`):** 2.0–3.1 s on the SDK, mostly from importing `mcp`/pydantic; 0.12–0.15 s on the fallback.
- **The 41 tool calls:** median 10 ms on the SDK and 5 ms on the fallback. The slowest call was 0.35 s
  (`get_invariant_reactions("Al-Zr", limit=200)`).
- **Whole session wall time:** 4.8–6.3 s on the SDK and 1.4–1.8 s on the fallback.

### Key numbers
Columns, left to right: accepted literature invariants (all records in brackets); SGTE diagrams; calculated
invariants per assessment; of those, how many have a literature match (same phase set), how many have an
experimental match, and how many experimental matches fall within 10 K; and the median |dT| of the best
experimental match.
| system | lit. invariants accepted (all) | SGTE diagrams | calc. invariants / lit. match / exp. match / exp. within 10 K | median \|dT\| best exp. match |
|---|---|---|---|---|
| Al–Cu | 80 (83) | 5 | 02Mie 7/4/3/2 · 04Wit 14/1/0/0 · 15Lia 17/7/7/4 · 21Kro 19/13/11/9 · 98Sau-LB 14/1/0/0 | 1.4 · – · 9.3 · 1.7 · – K |
| Al–Si | **0 (9)** | 5 | 1/0/0/0 each (eutectic 850.1–853.3 K) | – |
| Al–Mg | 31 (31) | 10 | 4–7 calc.; 3–5 lit.; 0–4 exp. matches | 0.1–1.7 K |
| Al–Zr | 178 (182) | 8 | 12–16 calc.; 12–14 lit.; 8–13 exp.; 5–13 within 10 K | 0.7 (01Wan) – 12.7 (86Sau) K |
| Cu–Ni | 0 (2) | 4 | 0 (isomorphous, correct) | – |

- **Peritectic and eutectic temperatures.** The Al–Zr peritectic L + Al3Zr → (Al) comes out at 929.7–934.1 K in all
  8 assessments, and every one matches literature within 1.05 K. The Al–Mg eutectic L → (Al) + β comes out at
  718.9–728.5 K, and all 10 assessments match literature (only 93Zuo matches an experimental record, at −0.84 K).
- **`phase_at`, 9 points.** Over all assessments the 9 points gave 54 answers. Leaving out the dilute Al–Zr point
  (finding 5), 44 of 46 matched what we expected: FCC_A1 at Al–2Cu/800 K, θ AL2CU_C16 at Al–33Cu/700 K,
  FCC_A1+DIAMOND_A4 at Al–10Si/800 K, LIQUID at Al–12.6Si/900 K, FCC_A1 at Al–5Mg/700 K, AL3ZR_D023 at Al–25Zr/1000 K,
  and FCC_A1 then LIQUID for Cu–30Ni/1000 K and Cu–50Ni/1650 K. The two exceptions are AlCu-02Mie, which gives
  `BCC_A2` at Al–33Cu (finding 4), and AlCu-21Kro, which gives FCC_A1+θ at Al–2Cu/800 K. The second is right at the
  solvus, so it is plausible.
- **`list_tdb_files`, exact pair counts.** Al–Cu 5, Al–Si 6 (includes AlSi-24Zob-3g, which has no diagram), Al–Mg 11
  (includes 1 `manual`-tier file), Al–Zr 8 and Cu–Ni 4. All are `bundled` except that one. Files containing both
  elements, binary or higher: 24, 21, 24, 21 and 20.
- **`get_formation_enthalpy`, kJ/mol-atom.**
  - Al3Zr: 37 literature values (9 experimental, mean −46.7, median −48.4; 24 model; 4 DFT), plus 27 in other
    units. MP gives −47.01 and OQMD −47.08, both D0_23 on the hull.
  - Al2Cu: see the finding below.
  - Al3Mg2: nothing at x(Mg)=0.400. β is really Al140Mg89 at x=0.389, and the composition match tolerance is 2e-3.
- **`compare_to_dft`.** Al–Zr: 9 compounds, default subset n=45, MAE 5.61 (MP) and 5.60 (OQMD) kJ/mol-atom, mean
  residual (DFT − literature) +3.6. Al–Cu, Al–Si, Al–Mg and Cu–Ni return no compounds, because there are no accepted
  literature HM_FORM values at DFT compositions. The 11 Al–Mg formation records are all DFT end-member values.

### Problems and findings, with exact lines
1. **No accepted Al–Si invariants.** Al–Si has 13 literature records and none is accepted, even though there are 8
   records of the 850.15 K eutectic. With `source="literature"` the call fails:
   `Error executing tool get_invariant_reactions: no invariant data for AL-SI`. Cu–Ni fails the same way
   (`... no invariant data for CU-NI`). The cause is the data gate: those records have
   `{'code': 'state_phases_missing', 'detail': 'INVARIANT_TEMPERATURE without the phases of its state (reactions_in_quote:0)', 'effect': 'not_accepted', 'gate': 'R3'}`,
   or their phases are not mapped to a model (`('Liquid', None), ('fcc-Al', None), ('diamond', None)`). The cause is
   in orchid-data, not the server; `source="both"` returns the calculated invariants alone.
2. **The Al–Cu eutectic L → (Al) + θ never matches literature.** It is calculated at 820.6–821.7 K in all 4
   assessments that model θ. Literature record `ORC-FNCFSLFUOM` (820.7 K) maps `('AlCu-θ', None)` and carries
   `label_conflicts_composition: AlCu-θ printed x(CU)=0.318, formula 0.5`: the phase label "AlCu-θ" was parsed as
   the formula AlCu. Experimental record `ORC-NHZUNBHOEB` (823.15 K) has no phases (gate R3). This is the key invariant
   for Al–Cu alloys, so it is a data bug worth reporting to orchid-data.
3. **Matching depends on phase names.** It requires the exact model phase set, so AlCu-04Wit and AlCu-98Sau-LB match
   1 of 14 invariants each. Their names are AL4CU9_D82 and ALCU_ETA; the literature is mapped to GAMMA_D82 and
   ALCU_ETA_HT, as in 21Kro. A low match count can mean naming, not disagreement.
4. **The Cu-side assessment AlCu-02Mie is computed and served over the whole composition range** with
   `status: "ok"` and no warning. Its TDB has only `AL4CU9_GAMMA, BCC_A2, FCC_A1, HCP_A3, LIQUID`, with no θ or η, so
   `phase_at` at x(Cu)=0.33 and 700 K returns `["BCC_A2"]`. The diagram also has an FCC_A1+HCP_A3+LIQUID invariant
   at 881 K on the Al-rich side, which does not exist. Do not use it for Al-rich alloys.
5. **The stored grid is too coarse for dilute alloys** (dx = 0.01, dT = 10 K). x(Zr)=0.002 snaps to the pure-Al
   column. Questions about dilute solubility, such as Zr, Sc or Mn in Al, need pycalphad run on the TDB. At that
   point, 18Tam answers `AL3ZR_D023+FCC_A1` and the other seven assessments answer `FCC_A1`.
6. **The DFT "lowest" value for Al2Cu is not θ.** `dft_mp_lowest` −17.18 and `dft_oqmd_lowest` −16.88 kJ/mol-atom both
   come from a theoretical 3-atom Fm-3m (fluorite-type) entry. θ (I4/mcm) lies 12.5 meV/atom above the MP hull, at
   −15.97 kJ/mol-atom. This is the known zero-kelvin ordering problem (doi:10.1103/PhysRevLett.86.5518, "Entropically
   favored ordering: the metallurgy of Al2Cu revisited"). ORCHID has no literature HM_FORM for Al2Cu, even with
   `accepted_only=false`.
7. **The README size table is out of date.** For CU-ZR, measured payload versus README "after":
   - `get_system_data`: 83,240 B vs 23,234 (3.6×)
   - `get_invariant_reactions`: 149,078 vs 83,218 (1.8×)
   - `get_formation_enthalpy("CuZr2")`: 2.0×
   - `compare_to_dft`: 1.4×
   - the other three calls: within 10 %

   Al–Zr defaults are larger still (`compare_to_dft` 230 KB on the SDK), which is costly for LLM context. Details
   are in `data/mcp_readme_sizes_*.csv`.
8. **The fallback server sends twice the bytes.** It returns both `content[0].text` and an identical
   `structuredContent`, so its messages are about 2× the SDK's. The payloads themselves are identical.
9. **Error formats differ between back ends.** For the same bad assessment, the SDK returns
   `Error executing tool get_phase_diagram: assessment 'no-such-assessment' not found for AL-CU; available: ['AlCu-02Mie.tdb', ...]`
   and also writes it to stderr as `Tool 'get_phase_diagram' failed: ...`. The fallback returns
   `{"error": "assessment 'no-such-assessment' not found ..."}`.
10. **Minor points.**
    - In plain mode, `orchid-mcp --transport http` exits 2 with `streamable HTTP needs the MCP SDK: pip install mcp`,
      as documented.
    - The `[test]` extra leaves pytest unpinned (we got 9.2.0), while CI pins `pytest==9.1.1` on Python 3.13. We used
      3.12.3 with no problems.

**Files.**
- Scripts: `scripts/orchid_mcp_drive.py`, `scripts/orchid_mcp_probe.py`, `scripts/orchid_mcp_readme_sizes.py`.
- Logs: `logs/orchid-mcp-{install,tests-plain,tests-mcp,stdio-sdk,stdio-fallback,probe,cli,readme-sizes}.log`.
- Data:
  - `data/mcp_{alcu,alsi,almg,alzr,cuni}_responses.json`: trimmed responses, with citation author strings replaced
    by a pointer to the DOI.
  - `data/mcp_misc_responses.json`
  - `data/mcp_summary_{sdk,fallback}.json`
  - `data/mcp_call_timings_{sdk,fallback}.csv`
  - `data/mcp_probe_accepted_vs_all.json`
  - `data/mcp_invariants_sgte_vs_literature.csv`: 247 calculated invariants with their best literature and
    experimental matches.
  - `data/mcp_readme_sizes_{sdk,fallback}.csv`

## orchid-data

**What it is.** ORCHID's open data release v2026.10 (CC BY 4.0, 1.6 GB checkout, commit `c4ebfb65`, 2026-10-30). It holds
73,542 machine-extracted literature values from 1,321 papers, the SGTE-binary phase diagrams calculated with pycalphad,
MP/OQMD hulls, a phase registry, assessed phase assemblages and ESPEI 0.9.1 datasets. All of it is also published as 7
Parquet tables. The repo ships a contribution validator with tests (`contributions/`) and two ESPEI-bundle checkers
(`espei/check_weights.py`, `espei/check_fit.py`).

**Environment.** venv `/tmp/arroyave/venvs/orchid-data` (Python 3.12.3). CI pins Python 3.13 and `pytest==9.1.1`. The
validator is standard-library only, so 3.12 is enough. Everything below ran through `/tmp/sbx/clean` with
`OMP_NUM_THREADS=1`. The source checkout was only read: `git status --porcelain` is empty afterwards, with no
`__pycache__`. The contribution checks ran in a copy of the CI sparse checkout at `/tmp/arroyave/work/orchid-data-contrib`,
with `release-site/tools` copied from orchid-project.org `786f64f`.

```sh
uv venv --python 3.12 /tmp/arroyave/venvs/orchid-data
uv pip install --python /tmp/arroyave/venvs/orchid-data/bin/python pandas pyarrow duckdb "pytest==9.1.1" matplotlib jsonschema
uv pip install --python /tmp/arroyave/venvs/orchid-data/bin/python "espei==0.9.1"   # for espei/check_fit.py only (pulls pycalphad 0.11.2)
# the three CI steps of .github/workflows/contributions.yml, run in the work copy
python contributions/tools/orchid_contrib.py validate --require-release-tools --release-tools release-site/tools --json contribution-report.json
ORCHID_RELEASE_TOOLS=release-site/tools python -m pytest -q -p no:cacheprovider contributions/tests
python contributions/tools/orchid_contrib.py credit --check
# ESPEI bundle checks shipped in espei/ (read-only)
python espei/check_weights.py --bundle espei
python -I scripts/orchid_data_fit_preflight.py --bundle espei --tdb <sgte-binary>/AlCu-21Kro.tdb --system AL-CU \
       --folders experimental,invariants --workdir /tmp/arroyave/work/orchid-data-fitcheck/AL-CU
python espei/check_fit.py --bundle espei --selection /tmp/arroyave/work/orchid-data-fitcheck/AL-CU/selection.json
# our scripts (scripts/orchid_data_*.py)
python -I scripts/orchid_data_integrity.py --data <orchid-data>               # MANIFEST hashes, card counts vs data
python -I scripts/orchid_data_duckdb_card_examples.py --data <orchid-data>    # the card's DuckDB/pandas examples
python -I scripts/orchid_data_coverage.py --data <orchid-data> --out data     # the two CSVs
python -I scripts/orchid_data_coverage_figure.py --csv data/al-cu-coverage.csv --out figures/orchid-data-al-cu-coverage.png
```

**Outcome: PASS.** Every check the repo ships passes. All Parquet tables load, and both CSVs were produced.

| step | result | time |
|---|---|---|
| `orchid_contrib.py validate --require-release-tools` | `validated 4 file(s): 0 error(s), 0 warning(s)` | 8.7 s |
| `pytest contributions/tests` (with release tools, so the phase-rule tests run) | `20 passed in 0.26s`, 0 skipped | 0.6 s |
| `orchid_contrib.py credit --check` | `credit: up to date` | 0.05 s |
| `espei/check_weights.py --bundle espei` | 8,589 datasets, 6,256 weighted values, `"errors": []` | 6.4 s |
| `espei/check_fit.py`: Al–Zr, 29 experimental + invariant datasets vs AlZr-20Lon.tdb | `ready: true` | 15 s |
| `espei/check_fit.py`: Al–Cu, 3 datasets vs AlCu-21Kro.tdb; Al–Mg, 2 datasets vs AlMg-93Zuo.tdb | `ready: true` (both) | 11 s, 6 s |
| `espei/check_fit.py`: all Al–Cu datasets vs AlCu-21Kro.tdb; all Al–Mg datasets vs AlMg-23Hal.tdb | `ready: false`, `target_phases_missing` (see problem 4) | 12 s each |
| MANIFEST check: 7 tables, row counts + file SHA-256, 9 inputs incl. the 2,774-file SGTE aggregate | all match | 6.5 s |
| DATASET_CARD DuckDB and pandas examples (5 queries) | all run | 1.2 s |
| coverage + invariants CSVs (pandas, all 7 tables + `espei/index.csv` + assemblages + registry) | done | 3–6 s |

**Key numbers.** The release has 73,542 values, 66,551 accepted, 11,161 ESPEI-ready and 1,892 certified. The table below
shows accepted counts; full columns are in `data/al-cu-coverage.csv`, and the figure is
`figures/orchid-data-al-cu-coverage.png`.

| system | values accepted / all | accepted exp. / model / DFT | papers | accepted exp. invariants | ESPEI datasets | SGTE TDBs (calc. invariants) |
|---|---|---|---|---|---|---|
| Al–Cu | 107 / 114 | 50 / 54 / 0 | 4 | 30 | 10 | 5 (71) |
| Al–Si | **0 / 13** | 0 / 0 / 0 | 5 | 0 | 0 | 5 + 1 failed (5) |
| Al–Mg | 147 / 148 | 9 / 46 / 92 | 5 | 5 | 10 | 10 (56) |
| Al–Zr | 658 / 743 | 170 / 385 / 82 | 10 | 88 | 210 | 8 (115) |
| Cu–Ni | 31 / 38 | 31 / 0 / 0 | 2 | 0 | 0 | 4 (0) |
| Cu–Zr | 674 / 683 | 344 / 314 / 15 | 9 | 214 | 233 | 11 (131) |
| Al–Mg–Si | 59 / 59 | 22 / 37 / 0 | 1 | 22 | 2 | – |
| Al–Mn–Cr–Zr ternaries and quaternary | 2 / 8 (Al–Cr–Mn 0/6, Al–Cr–Zr 2/2, others 0) | 0 / 2 / 0 | 1 each | 0 | 0 | – |
| Cu–Al–Ni–Fe ternaries and quaternary | 32 / 46 (Al–Cu–Fe 18/18, Cu–Fe–Ni 14/14, Al–Fe–Ni 0/14, Al–Cu–Ni 0, Al–Cu–Fe–Ni 0) | all 32 accepted are `unspecified` PHASE_COMPOSITION | 1 each | 0 | 0 | – |

The `papers` column is distinct `paper_id` values (`lit_papers` in the CSV). The other
requested binaries are Al–Mn, Al–Cr, Al–Fe, Al–Ni, Al–Sc, Cu–Sn, Cr–Cu, Cu–Fe and Be–Cu, plus the subsystem binaries
Mg–Si, Cr–Mn, Mn–Zr, Cr–Zr and Fe–Ni. Their numbers are in the CSV.

ORCHID cross-checks each invariant against a CALPHAD model (the `plausibility` flag). For accepted experimental
invariants:

| system | pass | fail | not checked | median \|ΔT\| |
|---|---|---|---|---|
| Al–Cu | 30 | 0 | 0 | 2.0 K |
| Al–Zr | 47 | 12 | 29 | 4.8 K |
| Cu–Zr | 37 | 15 | 162 | 16.4 K |
| Al–Mg | 3 | 0 | 2 | – |

The card's DuckDB join (accepted experimental invariants against SGTE calculated invariants within 20 K) returns
Al–Cu 30 → 292 pairs, Al–Mg 5 → 187, Al–Zr 86 → 900 and Cu–Zr 189 → 3,802. Al–Si and Cu–Ni return nothing, because
neither has any accepted experimental invariant.

**`data/al-cu-literature-invariants.csv`** has 345 rows: Al–Cu 31, Al–Si 4, Al–Mg 5, Al–Zr 89, Cu–Ni 1 and Cu–Zr 215.
Cu–Al is the same system as Al–Cu (ORCHID names a system by its alphabetically sorted elements, e.g. `AL-CU`). It holds
every `literature_values` row with `property == "INVARIANT_TEMPERATURE"` and `evidence_class == "experimental"`. Rows
that are not accepted are kept and flagged, so filter on `accepted` (and `duplicate_of` empty) before use; 337 rows are
accepted. Columns:

- **Temperature:** `T_K` (kelvin), `T_C` (°C) and `temperature_printed` (as printed, often °C).
- **Reaction:** `reaction_printed`, `reaction_type` / `transition_kind` (ORCHID's class; often empty), `phases` (printed
  labels) and `model_phases` (CALPHAD names).
- **Composition (mole fraction, not at.%):** `x_component` is the second element of the system name, and
  `x_by_phase_mole_fraction` gives that element's mole fraction in each phase, as `phase=x; ...`. Values printed for the
  other element were converted with x = 1 − x_A, and entries with basis `unresolved` were left out. 320 rows have at
  least one composition (Al–Si and Cu–Ni rows have none). `compositions_json` holds the raw list.
- **ESPEI and model check:** `espei_ready`, `espei_certified`, and `plausibility_*` (ΔT against the named SGTE TDB).
- **Source:** `paper_doi` (the paper the value was read from), `paper_title`, `paper_year`, `measured_in_doi` (the
  original measurement, when resolved to a DOI), `measured_in_raw`, `cited_dois`, `origin`, `page` and `table_row`.
- **Review:** `reader_agreement` and `gate_failure_codes`.

Author names are left out on purpose.

**How the `data/al-cu-coverage.csv` columns are computed.** The Parquet tables are in `parquet/`. Rows are matched on
`system` (sorted uppercase elements; this is the system of the record's own state).

- **`lit_*`** come from `literature_values`:
  - `lit_values_all`: all rows. `lit_values_accepted`: `accepted`. `lit_values_accepted_unique`: also `duplicate_of`
    empty. `lit_papers`: distinct `paper_id`.
  - `lit_acc_{experimental,model,dft,unspecified}`: accepted rows by `evidence_class`.
  - `lit_espei_ready` / `lit_espei_certified`: `flag_espei_ready` / `flag_espei_certified`.
  - `lit_hm_form_exp_accepted`: `property == HM_FORM`, experimental and accepted. `lit_phase_composition_exp_accepted`:
    the same filter with `PHASE_COMPOSITION`.
- **`inv_*`** are rows with `property == INVARIANT_TEMPERATURE`. They are split into all, accepted, experimental
  (all / accepted / accepted with `duplicate_of` empty) and model accepted, plus counts by `plausibility_result`.
- **`espei_*`** come from `espei/index.csv`, one row per dataset file, counted by `folder`: `experimental`,
  `invariants`, `model`, `dft/literature`, `dft/mp`, `dft/oqmd`, `assessed`, and `derived/*` summed. `espei_values_total`
  is the sum of `n_values`.
- **`sgte_*`** come from `phase_diagram_index`: TDBs with `status == ok`, TDBs with any other status (failed), and the
  file names. `sgte_calc_invariants` counts `phase_diagram_invariants` rows over all of the system's TDBs.
- **Other sources:**
  - `assessed_assemblage_points`: rows of `assessed-phase-assemblages/records.parquet`.
  - `phase_registry_phases`: `len(phases)` in `phases/systems/<SYS>.json`.
  - `hull_vertices_{mp,oqmd}`: `hull_vertices` rows that are not endpoints.
  - `dft_parity_rows` / `dft_parity_default_subset`: from `dft_parity`.

**Problems found**

1. **The dataset card has stale counts.** `DATASET_CARD.md` and its identical copy `hf/README.md` say "There are 73,538
   values …", "72,359 values are accepted", "covering 1,405 chemical systems", and evidence classes 36,268 / 26,214 /
   5,807 / 5,249. The Parquet tables, the JSONL dump and `literature/index.json` all give 73,542 values, **66,551
   accepted**, 1,474 systems and 36,288 / 26,153 / 6,150 / 4,951, and so does the current `CHANGELOG.md` headline. The
   card's numbers match an earlier CHANGELOG step ("Records 74,474 -> 73,538; accepted 73,165 -> 72,359"). It overstates
   accepted values by 5,808 (about 8 %) (`logs/orchid-data-integrity.log`).
2. **No Al–Si value is accepted** (0 of 13), which matters for AlSi10Mg. Twelve rows fail the gate
   `state_phases_missing`: the eutectic temperature around 850 K was read without its phases, so under the rule "A state
   needs real phases" it is not accepted. The 13th, `ORC-G7QZYNERF5` ("Liquid -> fcc-Al + diamond", 850.1 K, model), has
   `row_state = disputed_in_review_queue` and no `paper_doi`. `ORC-VHPE4TM3SI` ("Al3 V + Si2 V → L + τ") is an Al–Si–V
   reaction filed under AL-SI.
3. **Al–Cu coverage is thin.** It rests on 4 source papers (3 with a DOI), has no formation enthalpies of any evidence class (so nothing for
   θ-Al2Cu), and has no DFT-parity rows. A `get_formation_enthalpy("Al2Cu")` call to orchid-mcp therefore has no
   literature value to return. Nickel aluminium bronze (Cu–Al–Ni–Fe) and Al–Mn–Cr–Zr have essentially no data above
   binaries: no accepted experimental values and no invariants.
4. **ESPEI datasets carry the phase names of the TDB they were linked to**, so mixing assessments fails the preflight.
   Selecting every Al–Cu `experimental`+`invariants` dataset against AlCu-21Kro.tdb gives
   `{"code": "target_phases_missing", "path": "invariants/AL-CU/AlCu-02Mie.zpf-00.json", "phases": ["AL4CU9_GAMMA"]}`.
   Al–Mg against AlMg-23Hal.tdb fails with `AL8MG5_BETA`, `ALMG_ZETA` (from `AlMg-93Zuo.zpf-*`). Each passes against its
   own TDB. This is the checker working as documented, but a user fitting one target TDB must map phase names first.
   The receipts are in `data/orchid-data-preflight/`.
5. **Smaller issues:**
   - `phase_diagram_index` marks `AlSi-24Zob-3g.tdb` as `status: failed`, along with 3 Al–Mn TDBs and 1 Al–Cr TDB.
   - The Cu–Ni SGTE diagrams have 0 calculated invariants. That is expected, since the system is isomorphous apart from
     a miscibility gap. The one "experimental invariant" ORCHID records for Cu–Ni (1385 K, no phases) is gated out.
   - AlZr-10Hir's DOI in `phase_diagram_index` contains an en dash (`10.1515/HTMP.2010.29.5–6.347`). It is probably a
     typographic substitute for a hyphen; not checked online.
   - The `ESPEI` install pulls `emcee`, which emits `SyntaxWarning: invalid escape sequence '\e'` (harmless).

Logs: `logs/orchid-data-{contrib-validate,contrib-pytest,contrib-credit,espei-check-weights,espei-check-fit,integrity,duckdb-card-examples,coverage}.log`.

## orchid-bench

**What it is.** It is a ground-truthed pilot benchmark for ORCHID's extraction tools. It holds 20 synthetic "papers" (86 pages), one per SGTE binary, each generated with pycalphad 0.11.2. Each paper is rendered four ways (vector PDF, 300 dpi PNG, degraded 150 dpi JPEG and image-only PDF) and comes with an exact JSON truth key. The repo also ships a scorer (`bench/score.py`), the outputs of 19 extractors with their `scores.json`, and `results/RESULTS.md`. Al/Cu documents include AlCu-02Mie, AlSi-12Tan, AlMg-12Tan, AlNi-14Zhu, CuNi-87Jan, CuZn-08Gie, CuMg-16Hal, CuPb-86Hay-LB, AgCu-06He, AlZn-93Mey-LB and AlBi-06Kim.

**Environment and commands.** The repo ships no `requirements.txt` or `pyproject.toml`. Its README names `~/orchid-py313/bin/python` with "pycalphad 0.11.2, matplotlib, numpy, scipy, Pillow, PyMuPDF, pdfplumber". I installed those unpinned, except pycalphad:

```sh
/tmp/sbx/clean bash -c 'uv venv --python 3.13 /tmp/arroyave/venvs/orchid-bench && \
  uv pip install --python /tmp/arroyave/venvs/orchid-bench/bin/python "pycalphad==0.11.2" matplotlib numpy scipy pillow pymupdf pdfplumber sympy'
# resolved: pycalphad 0.11.2, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, pymupdf 2.1, pdfplumber 0.11.10, pillow 13.0.0
cp -a /tmp/arroyave/src/orchid-calphad__orchid-bench /tmp/arroyave/work/orchid-bench
# all steps through the driver (writes only to the work copy and results/):
/tmp/sbx/clean .../venvs/orchid-bench/bin/python -I scripts/orchid_bench_run.py rescore|oracle|baselines|provenance|results|results-ledger|generate 2
/tmp/sbx/clean .../venvs/orchid-bench/bin/python -I scripts/orchid_bench_pdfcompare.py
/tmp/sbx/clean bash scripts/orchid_bench_private_routes.sh
/tmp/sbx/clean .../venvs/orchid-bench/bin/python -I scripts/orchid_bench_alcu_table.py
```

`ORCHID_TDB_DIR` points at `orchid-project.org/data/databases/sgte-binary` and `ORCHID_PD_DIR` at `orchid-data/phase-diagrams/sgte`. `ORCHID_PIPELINE` is set to a path that does not exist, because the pipeline is a private repo. No LLM API was called: `bench/ai/run_gemini.py` needs `GEMINI_API_KEY` and spends money, so it was not run. The archived answers in `bench/ai/answers/` were only re-scored.

**Outcome: PARTIAL.** The public half of the benchmark reproduces: the scorer, the oracle self-test, the generator and truth keys, the pdfplumber baseline and the results tables. Everything else needs the private `orchid-pipeline` or Tesseract: the OCR, raster, Camelot and OpenCV routes, the AI-reader prepare/map stages and the showcase.

| step | time | result |
|---|---|---|
| install (cached wheels) | 2 s | OK; uv downloaded CPython 3.13.18 |
| re-score all 19 shipped extractor outputs (762 output files) with `score.py` | 61 s total | **19/19 run.** 10 `scores.json` byte-identical; the other 9 differ only by float rounding (max \|Δ\| = 1.1e-16 in 3–36 leaves) |
| oracle self-test (`baselines/oracle.py` + score) | 1.7 s + 16.5 s | **80/80 oracle files byte-identical** to shipped; all 188 aggregate ratio metrics = 1.0; scores identical to shipped |
| `baselines/tables_pdfplumber.py` (vector PDFs) | 15–17 s | **20/20 outputs byte-identical**; re-score identical to shipped (cells exact 0.759, invariant rows recall 0.592 on vector) |
| `baselines/text_regex.py` | 2 s | **FAIL** without the Tesseract cache (see problems). Its vector route, re-run through `scripts/orchid_bench_text_regex_vector.py` (pdfplumber text plus the repo's own `extract()`), gives **20/20 outputs byte-identical** and the same scores (precision 0.847, recall 0.973) |
| `generate.py --jobs 2` (20 docs, 86 pages, from shipped `bench/cache`) | 96 s | PNG 85/86, JPEG 86/86 and figure PDFs 80/80 byte-identical. `vector.pdf` and `image_only.pdf` are 0/20 byte-identical, but all 40 have identical page text and are **pixel-identical** at 72 dpi; they differ by 0–5 bytes, which points to PyMuPDF serialization. The truth keys differ only in the recorded SHA-256 of those PDFs plus 1 PNG. One PNG (CuZn-08Gie p.4) differs in 11 pixels (max 7/255) |
| provenance: truth-key SHA-256 vs local inputs | <1 s | 20/20 SGTE TDBs match `orchid-project.org/data/databases/sgte-binary`. 19/20 ORCHID diagram JSONs match orchid-data; `CuZn-08Gie.json` has changed in orchid-data since the benchmark was generated |
| `results/build_results.py` | 0.5–1.8 s | `RESULTS.md` and `results.json` **byte-identical** only after copying `results/gemini_ledger.jsonl` into `work/ai/` (bug below) |

**Key numbers.** The re-scored headlines equal `RESULTS.md`:
- ai_gemini invariant-row recall: 0.986 / 0.986 / 0.845 / 0.845 (vector / clean / degraded / image-only).
- pdfplumber table cells exact: 0.759.
- vector_route boundary recall@0.01: 0.886.
- ai_gemini field precision: 0.786 / 0.663 / 0.654 / 0.644.

Per-document scores for the 11 Al/Cu papers are in `data/orchid-bench-alcu-per-doc.csv` (165 rows):
- **Al–Cu (syn-AlCu-02Mie, vector):** Gemini recovers 8/8 invariant rows. Boundary recall@0.01 is 0.944; field recall/precision is 1.00/0.86. Diagram-invariant recall is 0.83, but precision is only 0.45 (11 predicted vs 6 true).
- **Cu–Ni (syn-CuNi-87Jan):** pdfplumber matches 0/2 rows and Gemini 1/2.
- **Al–Si:** pdfplumber matches 0/1 rows.

**Problems found (exact error lines):**
1. **No dependency manifest.** There is no requirements or lock file, and only pycalphad's version is stated, so byte-reproducing the PDFs needs the original PyMuPDF version (unknown).
2. **`text_regex.py` hard-requires the Tesseract OCR cache.** `bench/work/` is git-ignored and not shipped, so the script crashes even for the vector rendering: `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/arroyave/work/orchid-bench/bench/work/ocr/syn-AgCu-06He-v0/image_only_pdf/page-1.tsv'`. `baselines/ocr_cache.py` itself fails with `FileNotFoundError: [Errno 2] No such file or directory: 'tesseract'`. It also hard-codes `PATH=/opt/homebrew/bin:/usr/bin:/bin`, which is macOS-first. Tesseract was not installed here: it is a runtime dependency, not a build dependency, so the sudo/apt policy didn't cover it. The raster renderings of text_regex were therefore not re-run.
3. **`results/build_results.py` reads the Gemini ledger from the git-ignored `work/ai/gemini_ledger.jsonl`**, while the repo ships it as `results/gemini_ledger.jsonl`. On a fresh clone the "AI spend" table is rebuilt as all zeros (`| **total** | 0 | 0 | 0 | 0 | 0 | **0.00** | 0.00 |` instead of 525 calls / $8.46). Copying the file into `work/ai/` restores byte-identity.
4. **Private-pipeline stages fail at import:**
   - `vector_figures.py`, `tables_camelot.py`, `raster_xy.py`: `ModuleNotFoundError: No module named 'thermo_extractor'`.
   - `assessed_pd_raster.py`, `raster_pd.py`, `showcase/build.py`: `No module named 'assessed_pd'`.
   - `ai/prepare.py`: `No module named 'gemini_table_reader'`.
   - `ai/map_outputs.py`: `No module named 'text_reader_v6'`.
   - `ocr_pdf.py`: missing `tesseract`.

   The README says this ("The AI and raster routes need the private pipeline").
5. **Silent failures.** Without the pipeline, `baselines/tables_ocr.py` and `baselines/tdb_topology.py` exit 0. `tables_ocr.py` overwrote all 80 `outputs/ocr_table_cells/*.json` with empty results whose status reads `failed ... can't open file '/nonexistent/orchid-pipeline/scripts/ocr_table_cells.py'`; I restored them from the source. `tdb_topology.py` hard-codes `Pool(8)`.
6. **Generation.** It runs at about 96 s with 2 jobs; the README quotes "~10 s" with 8 jobs. Truth keys pin the ORCHID diagram SHA-256, and orchid-data's current `CuZn-08Gie.json` no longer matches it. That only matters if `bench/cache` is rebuilt (`CACHE_VERSION = 12`).

Logs: `logs/orchid-bench-{install,rescore,oracle,baselines,provenance,results,results-ledger,generate,generate-pdfcompare,private-routes}.log`. Data: `data/orchid-bench-{rescore,oracle,baselines,provenance,generate,generate-pdfcompare,results-rebuild-fresh-clone,results-rebuild-with-ledger}.json`, `data/orchid-bench-alcu-per-doc.csv`. Scripts: `scripts/orchid_bench_run.py`, `scripts/orchid_bench_pdfcompare.py`, `scripts/orchid_bench_private_routes.sh`, `scripts/orchid_bench_alcu_table.py`, `scripts/orchid_bench_text_regex_vector.py` (log `logs/orchid-bench-text-regex-vector.log`).

## orchid-project.org

**What it is.** This is the ORCHID website: static GitHub Pages HTML, `data/catalog.*` and redistributable TDBs, including the 2,776 files in `data/databases/sgte-binary/`. It also holds the release tooling (`tools/`, about 90 scripts: page builders, Parquet builder, Zenodo release, literature gates) with its own test suite (`tools/tests/`, 46 files). CI (`.github/workflows/tests.yml`) runs only `tools/tests/test_report_links.py`. Its own comment says "the full suite needs orchid-data".

**Environment and commands.** The source is read-only, so everything ran in copies. The full test suite ran in `/tmp/arroyave/work/orchid-project.org`. The second round of tests and the build checks ran in `/tmp/arroyave/work/site_siblings/`, which holds a site copy, a full 1.6 GB copy of orchid-data, and `open-tdb` as a symlink to the site's `data/`. `HOME` was a sandbox whose `~/projects/{orchid-data,open-tdb,orchid-examples}` link to the local checkouts.

```sh
/tmp/sbx/clean bash -c 'uv venv --python 3.13 /tmp/arroyave/venvs/orchid-site && \
  uv pip install --python /tmp/arroyave/venvs/orchid-site/bin/python "pytest==9.1.1" numpy pandas pyarrow pycalphad espei matplotlib'
# resolved: pytest 9.1.1 (CI pin), espei 0.9.1, pycalphad 0.11.2, pyarrow 26.0.1, pandas 3.1.1, numpy 2.5.4
HOME=/tmp/arroyave/work/site_home /tmp/sbx/clean .../venvs/orchid-site/bin/python -I scripts/orchid_site_tests.py ci   # CI test only
HOME=/tmp/arroyave/work/site_home /tmp/sbx/clean .../venvs/orchid-site/bin/python -I scripts/orchid_site_tests.py      # all 46 files
HOME=... /tmp/sbx/clean env ORCHID_SITE_DIR=/tmp/arroyave/work/site_siblings/orchid-project.org \
  .../python -I scripts/orchid_site_tests.py test_diagram_recovery.py test_precision_sample.py test_contributions_hook.py
HOME=... /tmp/sbx/clean bash scripts/orchid_site_build_checks.sh    # static pages, site numbers, Parquet, Zenodo plan/scan/manifest/metadata/card
HOME=... /tmp/sbx/clean bash scripts/orchid_site_build_checks2.sh   # 10 more builders' --check modes
```

The driver runs each test file on its own, with a 240 s timeout. Files that define `test_*` run under pytest; the rest are scripts that print PASS/FAIL lines. `ORCHID_DATA`, `ORCHID_LITERATURE` and `ORCHID_PARITY` point at orchid-data. I ran nothing that publishes or deploys: no `zenodo_release.py bundle`, `writeback` or `credit`. A file-modification scan after every run found **no writes** to the shared orchid-data, orchid-project.org or orchid-examples sources.

**Outcome: PASS for tests; PARTIAL for the build checks.** The build checks fall short for two reasons. Some committed artefacts are stale relative to the current tooling or data: `phases/index.html`, the Zenodo metadata, the Kim 2017 cross-check and the ESPEI bundle. And five builders need upstream inputs that are not published.

| step | time | result |
|---|---|---|
| install (cached) | 2 s | OK |
| CI test `test_report_links.py` | 0.9 s | **3 passed** |
| full suite, first pass: 46 files (21 pytest, 25 script) | 375 s | 44/46 exit 0 and 1 test skipped. The 2 failures and the skip all come from repo-layout assumptions, listed under problems |
| the 3 affected files with siblings `../open-tdb`, `../orchid-data` and `data/literature` | 19 s | 12 passed; 27 PASS / 0 FAIL; 1 passed |
| **suite total with the sibling layout** | ~395 s | **46/46 files pass: 150 pytest tests and 713 script PASS lines, 0 FAIL.** The `FAIL:` line printed inside `test_zenodo_writeback.py` is that script's own expected output from a negative test ("PASS leftover placeholder fails writeback") |
| `build_static_pages.py --check` | 74 s | **OK: 24,347 files current (18,295 HTML pages)** |
| `build_parquet.py --check` | 103 s | **parquet/ is up to date (7 tables)**: the Parquet release rebuilds identically from the JSON |
| `zenodo_release.py scan` | 170 s | **SCAN OK** (no restricted file type or path, no secret pattern) |
| `zenodo_release.py card --check` | 0.1 s | dataset card current |
| `build_site_numbers.py --check` | 1.4 s | **FAIL**: `stale: phases/index.html` / `FAIL: 1 problem(s)` |
| `zenodo_release.py metadata --check` | 4 s | **FAIL**: stale metadata for 9 of the 10 records |
| `zenodo_release.py plan` and `manifest --check` | 6–7 s | **FAIL** (environment): the examples repo is pinned at a commit missing from the depth-1 clone |
| `add_cite_as.py --check` / `phase_aliases.py --check` | 0.7 s / 5.8 s | current / "64 aliases in 32 systems; 0 problems" |
| `build_precision_sample.py --check` | 9 s | "precision sample frozen and intact (… 300 items …)". It also reports 210 sampled items whose released value has changed since sampling |
| `kim2017_crosscheck.py --check` | 3 s | **stale** (`data/literature/kim2017_crosscheck.json`, `.md`). See problem 7 |
| `build_espei_bundle.py --check` | 164 s | Runs once a separate ESPEI venv exists at `~/.venvs/espei/bin/python`, which I created with unpinned espei 0.9.1. Evaluation pass 1 gives `{'ok': 3285, 'error': 200, 'tdb_error': 3}`; pass 2 gives `{'ok': 3285}`. Verdict: **`out of date: 9 changed/missing, 5304 stale`**, probably ESPEI/pycalphad version drift; the authors' versions are not pinned |
| `build_phase_registry`, `build_bibliography`, `build_dft_parity`, `build_assessed_assemblages`, `export_literature_data` `--check` | 0.2–12 s | **NOT RUNNABLE**: each needs unpublished upstream build inputs (problem 8) |

**Slowest tests.** These read the full literature release: test_release_integrity (44 s), test_r2_thermo (38 s), test_phase_rule (38 s), test_r2_compositions (35 s), test_r3 (32 s) and test_r2_phases (31 s).

**Problems found (exact error lines):**
1. **The tests assume sibling checkouts.** Several paths ignore `OPEN_TDB` and `ORCHID_DATA`:
   - `test_diagram_recovery.py` resolves `Path(__file__).resolve().parents[3] / "open-tdb/databases/sgte-binary/MgY-98Luk.tdb"` and fails with `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/arroyave/work/open-tdb/databases/sgte-binary/MgY-98Luk.tdb'`.
   - `test_precision_sample.py` needs the git-ignored `data/literature/` local copy: `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/arroyave/work/orchid-project.org/data/literature/orchid-literature.jsonl.gz'`.
   - `test_contributions_hook.py` is skipped with `orchid-data with contributions/ not found next to this repository`.

   All three pass once `../open-tdb`, `../orchid-data` and `data/literature` exist.
2. **The suite mixes styles.** 25 of the 46 files are scripts with module-level code, and some call `argparse` at import, so `pytest tools/tests` cannot run the suite. Each script has to be run with `python`. Only 1 file runs in CI.
3. **A stale committed page.** `build_site_numbers.py --check` gives `stale: phases/index.html`. Regenerating it adds only the builder's new "please also cite the SGTE collection (Hallstedt, Calphad 89 (2025) 102833)" paragraph, so the committed page predates the current builder.
4. **Stale Zenodo metadata in orchid-data.** `metadata --check` gives `stale Zenodo metadata: zenodo/orchid-data.metadata.json, zenodo/literature.metadata.json, ... zenodo/orchid-examples.metadata.json` (9 records; `assessed-phase-assemblages` is current). Regenerating them in the copy shows that the site tooling now credits MaterialsFramework: it adds a description paragraph and 2 related identifiers per record, a GitHub URL and the Zenodo DOI 10.5281/zenodo.15731044. The committed metadata lacks both.
5. **The release plan pins orchid-examples at a commit we don't have.** `git rev-parse --verify 6d68789772775a74b55b54a1b3de62843899833f^{commit} failed in .../orchid-examples: fatal: Needed a single revision`. The local orchid-examples HEAD is `616b518` and the clone is shallow, so this may be an older commit rather than a missing one. Without the sibling link the error is `PROBLEM: examples repository not found at .../orchid-examples (--examples)`.
7. **A stale Kim 2017 cross-check.** I regenerated it in the orchid-data copy. The committed `kim2017_crosscheck.md` lists "1436 … records … over 606 formulas", but the current release gives 1452 over 610, so the committed file predates the latest literature export. The committed file also compares against a local copy of the Kim et al. 2017 Figshare CSV that the tool never downloads, so off the authors' machines the result is "**Status: not compared.**"
8. **Unpublished upstream inputs.** Five builders read files that exist only on the authors' machines or in the open-tdb build tree, which is not part of the release:
   - `build_phase_registry.py`: `FileNotFoundError: … '~/data/PD-extraction/sources/hallstedt2025_mmc2.xlsx'`.
   - `build_bibliography.py`: `… '~/projects/open-tdb/build/sgte-corpus/tdb_pdf_links.json'`.
   - `build_dft_parity.py` and `export_literature_data.py`: `… '~/projects/open-tdb/hulls/snapshot/snapshot.json'`.
   - `build_assessed_assemblages.py`: `… '~/projects/open-tdb/build/okamoto-annotation/run-20261021h-full/run_manifest.json'`.

   `build_espei_bundle.py` also hard-codes a second interpreter, `~/.venvs/espei/bin/python`: `FileNotFoundError: [Errno 2] No such file or directory: '…/.venvs/espei/bin/python'`.
9. **Hard-coded macOS paths.** `tools/run_all.sh` (the full SGTE diagram rebuild) is `#!/bin/zsh` and hard-codes `~/orchid-py313`, `~/projects/...` and `--workers 9`. I didn't run it: it recomputes every SGTE binary diagram, which is hours of CPU and outside the brief.

Logs: `logs/orchid-project.org-{install,ci-test,full-tests,sibling-tests,build-checks,build-checks2}.log`, `logs/orchid-project.org-tests-detail.log` (per-file output, trimmed) and `logs/orchid-project.org-build-checks-detail.log`. Data: `data/orchid-project.org-tests{,-ci,-siblings}.json`. Scripts: `scripts/orchid_site_tests.py`, `scripts/orchid_site_build_checks.sh`, `scripts/orchid_site_build_checks2.sh`.

## Summary

| repo | install | tests/examples run | outcome | notes |
|---|---|---|---|---|
| orchid-examples | OK (3 uv venvs, py3.12.3; all pins resolve on Linux) | 5 quick paths (strict + CI tolerance), hygiene, full-path rescoring of SGTE and GRACE Cu–Zr TDBs, quickstart re-run for Al–Cu/Al–Si/Al–Zr | PASS (CI tolerance) / strict sha256 FAIL on PNG bytes only | 3/4 JSON + 5/6 PDFs byte-identical (4th JSON differs only in a file hash); SGTE 0.722/0.728 and GRACE 0.426/0.410 reproduced with 315/315 identical predictions; scorer is Cu–Zr-only; committed grid hash is stale (CRLF) |
| orchid-mcp | PASS (uv, py3.12; plain 7 pkgs and `[mcp]` 35 pkgs, <1 s each) | pytest in 2 venvs × 2 modes (52/52 with data and SDK); stdio JSON-RPC on SDK and fallback, 41 tool calls × 5 systems | PASS | identical payloads on both back ends; Al–Si has 0 accepted invariants; the Al–Cu θ eutectic is unmatched (label-parse gate); AlCu-02Mie served Al-rich without warning; README size table stale |
| orchid-data | PASS (uv venv py3.12; pandas/pyarrow/duckdb, pytest 9.1.1; ESPEI 0.9.1 for check_fit) | contrib validate + 20 pytest + credit check; espei check_weights; check_fit ×5; MANIFEST hashes; card DuckDB examples; coverage + invariants CSVs | PASS | all shipped checks pass; DATASET_CARD counts stale (72,359 vs 66,551 accepted); Al–Si 0/13 accepted; Al–Cu has 4 papers and no ΔHf; no NAB or Al–Mn–Cr–Zr ternary data |
| orchid-bench | OK (uv, py3.13, pycalphad 0.11.2 + unpinned matplotlib/PyMuPDF/pdfplumber; no manifest in repo) | re-score 19 extractors; oracle self-test; pdfplumber + text_regex (vector) baselines; full regeneration of 20 docs; provenance; results rebuild; 12 private/OCR stages attempted | PARTIAL | scorer/oracle/pdfplumber/results reproduce exactly; regenerated docs pixel-identical (PDF bytes differ by 0–5 B); text_regex needs Tesseract; AI/raster/Camelot routes need the private orchid-pipeline; results builder reads the ledger from a git-ignored path; no LLM calls made |
| orchid-project.org | OK (uv, py3.13, pytest 9.1.1 + espei 0.9.1/pycalphad 0.11.2/pyarrow; no manifest, CI pins only pytest) | CI test; all 46 tools/tests files (150 pytest tests + 713 script checks); 18 offline `--check`/plan/scan builder runs | PASS (tests) / PARTIAL (build checks) | 46/46 test files pass once sibling `../open-tdb`, `../orchid-data` and `data/literature` exist (2 fail + 1 skip otherwise); static pages (24,347 files), Parquet (7 tables), cite_as, phase aliases and the precision sample are current; secret scan OK; `phases/index.html`, 9 Zenodo metadata files, the Kim 2017 cross-check and the ESPEI bundle are stale vs the tooling or the data; 5 builders need unpublished upstream inputs; the release plan pins an orchid-examples commit absent from the shallow clone; nothing published |

## Files

All paths are relative to this folder (`sections/` holds the per-repo sources of this report).

- `data/al-cu-coverage.csv`, `data/al-cu-literature-invariants.csv`, `data/mcp_alcu_responses.json`, `data/mcp_almg_responses.json`, `data/mcp_alsi_responses.json`, `data/mcp_alzr_responses.json`, `data/mcp_call_timings_fallback.csv`, `data/mcp_call_timings_sdk.csv`, `data/mcp_cuni_responses.json`, `data/mcp_invariants_sgte_vs_literature.csv`, `data/mcp_misc_responses.json`, `data/mcp_probe_accepted_vs_all.json`, `data/mcp_readme_sizes_fallback.csv`, `data/mcp_readme_sizes_sdk.csv`, `data/mcp_summary_fallback.json`, `data/mcp_summary_sdk.json`, `data/orchid-bench-alcu-per-doc.csv`, `data/orchid-bench-baselines.json`, `data/orchid-bench-generate-pdfcompare.json`, `data/orchid-bench-generate.json`, `data/orchid-bench-oracle.json`, `data/orchid-bench-provenance.json`, `data/orchid-bench-rescore.json`, `data/orchid-bench-results-rebuild-fresh-clone.json`, `data/orchid-bench-results-rebuild-with-ledger.json`, `data/orchid-bench-results-rebuild.json`, `data/orchid-data-preflight/AL-CU-21Kro-only.receipt.json`, `data/orchid-data-preflight/AL-CU.receipt.json`, `data/orchid-data-preflight/AL-MG-93Zuo.receipt.json`, `data/orchid-data-preflight/AL-MG.receipt.json`, `data/orchid-data-preflight/AL-ZR.receipt.json`, `data/orchid-examples-headlines.csv`, `data/orchid-examples-oneshot-rescore.json`, `data/orchid-project.org-tests-ci.json`, `data/orchid-project.org-tests-siblings.json`, `data/orchid-project.org-tests.json`
- `figures/orchid-data-al-cu-coverage.png`
- `logs/orchid-bench-baselines.log`, `logs/orchid-bench-generate-pdfcompare.log`, `logs/orchid-bench-generate.log`, `logs/orchid-bench-install.log`, `logs/orchid-bench-oracle.log`, `logs/orchid-bench-private-routes.log`, `logs/orchid-bench-provenance.log`, `logs/orchid-bench-rescore.log`, `logs/orchid-bench-results-ledger.log`, `logs/orchid-bench-results.log`, `logs/orchid-bench-text-regex-vector.log`, `logs/orchid-data-contrib-credit.log`, `logs/orchid-data-contrib-pytest.log`, `logs/orchid-data-contrib-validate.log`, `logs/orchid-data-coverage.log`, `logs/orchid-data-duckdb-card-examples.log`, `logs/orchid-data-espei-check-fit.log`, `logs/orchid-data-espei-check-weights.log`, `logs/orchid-data-integrity.log`, `logs/orchid-examples-full-oneshot-grace.log`, `logs/orchid-examples-full-oneshot-sgte.log`, `logs/orchid-examples-full-quickstart-AL-CU.log`, `logs/orchid-examples-full-quickstart-AL-SI.log`, `logs/orchid-examples-full-quickstart-AL-ZR.log`, `logs/orchid-examples-install.log`, `logs/orchid-examples-quick-ci-pixeltol-oneshot.log`, `logs/orchid-examples-quick-ci-pixeltol-phaseforgeplus.log`, `logs/orchid-examples-quick-ci-pixeltol.log`, `logs/orchid-examples-quick-cuzr-phaseforgeplus.log`, `logs/orchid-examples-quick-diffs.log`, `logs/orchid-examples-quick-quickstart.log`, `logs/orchid-examples-quick-small3.log`, `logs/orchid-mcp-cli.log`, `logs/orchid-mcp-install.log`, `logs/orchid-mcp-probe.log`, `logs/orchid-mcp-probe.stderr.log`, `logs/orchid-mcp-readme-sizes.log`, `logs/orchid-mcp-stdio-fallback.hashes.json`, `logs/orchid-mcp-stdio-fallback.log`, `logs/orchid-mcp-stdio-fallback.stderr.log`, `logs/orchid-mcp-stdio-sdk.hashes.json`, `logs/orchid-mcp-stdio-sdk.log`, `logs/orchid-mcp-stdio-sdk.stderr.log`, `logs/orchid-mcp-tests-mcp.log`, `logs/orchid-mcp-tests-plain.log`, `logs/orchid-project.org-build-checks-detail.log`, `logs/orchid-project.org-build-checks.log`, `logs/orchid-project.org-build-checks2.log`, `logs/orchid-project.org-ci-test.log`, `logs/orchid-project.org-full-tests.log`, `logs/orchid-project.org-install.log`, `logs/orchid-project.org-sibling-tests.log`, `logs/orchid-project.org-tests-detail.log`
- `scripts/assemble_report.py`, `scripts/orchid_bench_alcu_table.py`, `scripts/orchid_bench_pdfcompare.py`, `scripts/orchid_bench_private_routes.sh`, `scripts/orchid_bench_run.py`, `scripts/orchid_bench_text_regex_vector.py`, `scripts/orchid_data_coverage.py`, `scripts/orchid_data_coverage_figure.py`, `scripts/orchid_data_duckdb_card_examples.py`, `scripts/orchid_data_fit_preflight.py`, `scripts/orchid_data_integrity.py`, `scripts/orchid_examples_png_rms.py`, `scripts/orchid_examples_quickstart_system.py`, `scripts/orchid_mcp_drive.py`, `scripts/orchid_mcp_probe.py`, `scripts/orchid_mcp_readme_sizes.py`, `scripts/orchid_site_build_checks.sh`, `scripts/orchid_site_build_checks2.sh`, `scripts/orchid_site_tests.py`
