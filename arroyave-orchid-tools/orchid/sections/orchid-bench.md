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

| orchid-bench | OK (uv, py3.13, pycalphad 0.11.2 + unpinned matplotlib/PyMuPDF/pdfplumber; no manifest in repo) | re-score 19 extractors; oracle self-test; pdfplumber + text_regex (vector) baselines; full regeneration of 20 docs; provenance; results rebuild; 12 private/OCR stages attempted | PARTIAL | scorer/oracle/pdfplumber/results reproduce exactly; regenerated docs pixel-identical (PDF bytes differ by 0–5 B); text_regex needs Tesseract; AI/raster/Camelot routes need the private orchid-pipeline; results builder reads the ledger from a git-ignored path; no LLM calls made |
