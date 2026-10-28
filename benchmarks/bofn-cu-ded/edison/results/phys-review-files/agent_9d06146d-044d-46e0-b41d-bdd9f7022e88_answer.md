## Files Ready for Analysis

| File | Description | Format | Size |
|---|---|---|---:|
| `/workspace/outputs/added_lowNi.csv` | **85 measured records:** 74 mass-loss rates, 8 Tafel currents, 3 LPR currents; exact compositions, conditions and source locations | CSV | 84.5 KiB |
| `/workspace/outputs/audit_lowNi.md` | Primary evidence tables, Qian/Lewis source audits and limitations | Markdown | 20.1 KiB |
| `/workspace/outputs/audited_source_values.csv` | 17 verified Qian/Lewis source values, separate from primary additions | CSV | 4.8 KiB |
| `/workspace/outputs/lowNi_sources.bib` | Complete bibliography saved through e14c citation APIs | BibTeX | 4.5 KiB |
| `/workspace/downloads/lowNi/source_evidence.zip` | Supporting evidence: original PDFs, parsed papers, table images and access logs | ZIP | 76.4 MiB |
| `/workspace/outputs/source_manifest.json` | Provenance, endpoints, parameters, transformations and checksums for every evidence member | JSON | 83.7 KiB |
| `/workspace/outputs/curated_lowNi_records.json` | Source-verified transcription underlying additions | JSON | 165.2 KiB |
| `/workspace/outputs/reproduce_lowNi.py` | Rebuilds CSV; optional source refresh | Python | 3.3 KiB |
| `/workspace/outputs/validation_summary.json` | Record counts, integrity checks and unresolved limitations | JSON | 872 B |

### Key evidence recovered

**A primary same-study zero-Ni immersion bridge was found:** Reinhart’s original **1968 NCEL N-961** report contains matched seawater deployments comparing oxygen-free Cu, low-Ni Cu-Ni, 90/10, 70/30, no-Ni aluminum bronze and 4–5Ni NAB. Records preserve participant, deployment, actual depth, duration and composition.

**Important correction:** its “95-5” specimen contains **6.25 wt% Ni**, not measured 5% Ni. Exact Cu-2Ni/Cu-5Ni evidence remains unfilled; this substitution is explicitly flagged. These historical tests used cold, low-oxygen deep seawater—not warm surface seawater.

Modern low-Ni immersion evidence includes **Yang2018: 0.0215 mm/y** for Cu-7Ni-3Al-1Fe-1Mn versus the authors’ **0.0359 mm/y** C70600 comparator, with incomplete comparator protocol/product-form documentation flagged; and **Zhu2017: 0.028 mm/y**, 720 h, 3.5% NaCl, for Cu-6.5Ni-1Al-1Si-0.15Mg-0.15Ce.

### Audit status

**`/workspace/corrosion_data.csv` is absent.** Therefore, the deliverable is a source-level audit and standalone additions—not a completed row-by-row reconciliation, merge or deduplication.

- **Qian2025:** Tables 4–5 contain **Tafel current densities**, not measured immersion penetration rates. Actual B10/B30 chemistries and 3 h–7 d durations are recorded. Stray TP2 prose does **not** establish a measured pure-Cu control.
- **Lewis–LaQue1981:** a **review**, not a new 1981 test campaign. The audit separates rate ranges, unspecified durations, dimensionless rate ratios, pit depths and reproduced 60-day **3.4% NaCl** results.
- **Walsh2024:** supplies a same-test Cu/CuNi/NAB electrochemical bridge, but an internal Tafel/LPR numerical inconsistency is retained with explicit flags.

### File provenance and reproduction

- **`/workspace/outputs/added_lowNi.csv`** — derived from verified primary tables/passages in Reinhart1968, Yang2018, Zhu2017 and Walsh2024. Selection: within-study comparisons and low-Ni alloy measurements; original units retained. Only immersion mpy→mm/y conversion was applied (`×0.0254`); no fitting or constructed alloy controls.
- **`/workspace/outputs/audit_lowNi.md`** — source audit using DOI endpoints **10.1007/s42114-024-01174-0** and **10.2172/6255887**, plus the primary additions above; exact table/page references included.
- **`/workspace/outputs/audited_source_values.csv`** — Qian Tables 4–5 and Lewis Tables III/XX; source values/ranges retained, without invented durations or grade mappings.
- **`/workspace/outputs/lowNi_sources.bib`** — DOI metadata retrieved using `e14c.web.cite_doi`; report entries and verified catalog corrections saved using `save_citation`. API citation copy: `/workspace/citations/local-lowNi-audit/9d06146d-044d-46e0-b41d-bdd9f7022e88.bib`.
- **`/workspace/downloads/lowNi/source_evidence.zip`** — 112 evidence files plus an internal manifest. Principal downloads: [Reinhart1968](https://archive.org/download/corrosionofmater04rein/corrosionofmater04rein.pdf), [Reinhart1966](https://archive.org/download/DTIC_AD0644473/DTIC_AD0644473.pdf), [Reinhart1976](https://archive.org/download/corrosionofmetal00rein/corrosionofmetal00rein.pdf), [Lewis1981](https://www.osti.gov/servlets/purl/6255887), [Zhu2017](https://tnmsc.csu.edu.cn/EN/PDF/8533). Qian, Walsh and Yang full-paper snapshots were retrieved through `e14c.web.fetch_paper(doi=...)`. Original versions retained; PDF text extraction and table-image rotation documented. Every member’s absolute retrieval path, endpoint, parameters and transformations are listed in the manifest. Failed-access diagnostics are clearly distinguished from retrieved primary texts.
- **`/workspace/outputs/source_manifest.json`** — complete per-file provenance and SHA-256 inventory for the archive; retrieved 2026-10-28; genome build not applicable.
- **`/workspace/outputs/curated_lowNi_records.json`** — manually verified numeric transcription, including source composition limits, censored rates and quality flags; no normalization or interpolation.
- **`/workspace/outputs/reproduce_lowNi.py`** — reproduction code using the verified transcription and recorded HTTPS/API sources.
- **`/workspace/outputs/validation_summary.json`** — validation results: CSV regeneration was byte-identical; every archived evidence member passed CRC and SHA-256 verification.

Rebuild: `python /workspace/outputs/reproduce_lowNi.py`. Add `--refresh-sources` to repeat source retrievals.