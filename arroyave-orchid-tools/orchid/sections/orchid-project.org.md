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

| orchid-project.org | OK (uv, py3.13, pytest 9.1.1 + espei 0.9.1/pycalphad 0.11.2/pyarrow; no manifest, CI pins only pytest) | CI test; all 46 tools/tests files (150 pytest tests + 713 script checks); 18 offline `--check`/plan/scan builder runs | PASS (tests) / PARTIAL (build checks) | 46/46 test files pass once sibling `../open-tdb`, `../orchid-data` and `data/literature` exist (2 fail + 1 skip otherwise); static pages (24,347 files), Parquet (7 tables), cite_as, phase aliases and the precision sample are current; secret scan OK; `phases/index.html`, 9 Zenodo metadata files, the Kim 2017 cross-check and the ESPEI bundle are stale vs the tooling or the data; 5 builders need unpublished upstream inputs; the release plan pins an orchid-examples commit absent from the shallow clone; nothing published |
