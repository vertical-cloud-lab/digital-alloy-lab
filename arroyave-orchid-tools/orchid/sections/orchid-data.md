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

| orchid-data | PASS (uv venv py3.12; pandas/pyarrow/duckdb, pytest 9.1.1; ESPEI 0.9.1 for check_fit) | contrib validate + 20 pytest + credit check; espei check_weights; check_fit ×5; MANIFEST hashes; card DuckDB examples; coverage + invariants CSVs | PASS | all shipped checks pass; DATASET_CARD counts stale (72,359 vs 66,551 accepted); Al–Si 0/13 accepted; Al–Cu has 4 papers and no ΔHf; no NAB or Al–Mn–Cr–Zr ternary data |
