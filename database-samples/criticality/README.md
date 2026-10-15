# Materials Criticality Database Samples (Topic 3B)

Small sample downloads from the materials criticality databases catalogued in Section 3A of [alloy-databases.md](../../alloy-databases.md). These verify accessibility and show data format/schema for each source, supporting FLAIME's mineral-burden objective M(x) = Σ(wt%_i × CF_i) in the pKGFN pipeline for DOE Genesis Mission Topic 3B.

## Successfully Accessed & Downloaded

### 1. USGS Mineral Commodity Summaries (MCS) 2025
- **Source**: [USGS ScienceBase](https://www.sciencebase.gov/catalog/item/6793e234d34e72688d6b71e7) — Salient Commodity Data Release
- **Method**: ScienceBase REST API (`sciencebase.gov/catalog/item/{id}?format=json`), then direct file download
- **Files**: `usgs_mcs2025_*.csv` — production, imports, exports, consumption, prices, net import reliance for:
  - `usgs_mcs2025_alumi.csv` — Aluminum
  - `usgs_mcs2025_zirco.csv` — Zirconium and Hafnium
  - `usgs_mcs2025_chrom.csv` — Chromium (100% NIR — fully import-reliant)
  - `usgs_mcs2025_manga.csv` — Manganese (100% NIR)
  - `usgs_mcs2025_beryl.csv` — Beryllium
  - `usgs_mcs2025_cobal.csv` — Cobalt
  - `usgs_mcs2025_galli.csv` — Gallium
  - `usgs_mcs2025_scand.csv` — Scandium (100% NIR)
  - `usgs_mcs2025_rareee.csv` — Rare Earth Elements (>95% NIR)
- **Coverage**: 85+ commodities in the full zip (171 files), 2020–2024 data
- **Notes**: The full salient data zip (400 KB) contains CSV + XML metadata for all commodities. This is the authoritative US production/trade/price dataset used in virtually all criticality methods.

### 2. Mulukutla et al. SupplyRiskAwareDesign
- **Source**: [GitHub: mrinalinimulukutla/SupplyRiskAwareDesign](https://github.com/mrinalinimulukutla/SupplyRiskAwareDesign)
- **Method**: GitHub raw content API
- **Files**:
  - `mulukutla_supply_risk_scores.csv` — Elemental supply risk (SR) indices for Mo, Nb, Ti, V, W (0–100 scale)
  - `mulukutla_elemental_properties.csv` — Physical properties (atomic weight, density, electronegativity, melting T, valence electrons)
  - `mulukutla_S1.json` — LLM extraction configuration with prompts for production/reserve/resource statistics and S indicator calculation formula
- **Notes**: Closest direct precedent for criticality-aware alloy Bayesian optimization. The repo also contains LLM extraction pipeline code, Pareto front data, and MOBO integration. The `supply_risk/index.py` module computes weighted alloy-level supply risk from composition.

### 3. Matminer (Python package, v0.10.0)
- **Source**: `pip install matminer` — [matminer.org](https://hackingmaterials.lbl.gov/matminer/)
- **Method**: `matminer.datasets.load_dataset()` (downloads from Figshare) and `matminer.featurizers.composition.ElementProperty`
- **Files**:
  - `matminer_elastic_al_sample.csv` — 20 Al-based compounds with elastic properties (K_VRH, G_VRH, anisotropy, Poisson ratio) from DFT, from the 1,181-entry elastic_tensor_2015 dataset
  - `matminer_glass_binary_al_sample.csv` — 20 Al-containing binary metallic glass compositions with glass forming ability (GFA) labels, from the 5,959-entry glass_binary dataset
  - `matminer_steel_strength_sample.csv` — 10 steels with composition and yield/tensile strength, from the 312-entry steel_strength dataset
  - `matminer_magpie_features_sample.csv` — 7 alloys (Al, AlZr, Al3Zr, AlMnCrZr, CuCrZr, AlSi10Mg, Al5Mn) featurized with 132 Magpie composition features
- **45 built-in datasets** available including glass_binary (5,959 alloys), glass_ternary_landolt (7,191 experiments), elastic_tensor_2015 (1,181 DFT), steel_strength (312 steels), expt_gap (6,354 semiconductors), matbench_steels, etc.
- **Notes**: Matminer's `ElementProperty.from_preset('magpie')` generates 132 composition-based features per alloy — directly usable as input for ML/BO models. Also provides API wrappers for Materials Project, AFLOW, and other databases.

### 4. EU JRC RMIS (web page only)
- **Source**: [rmis.jrc.ec.europa.eu](https://rmis.jrc.ec.europa.eu/)
- **Method**: Web fetch (HTML page loaded successfully)
- **Notes**: RMIS portal is accessible but provides data primarily through interactive web dashboards and PDF factsheets — no public REST API found. The 2023 SCRREEN3 CRM Factsheets can be downloaded individually from the portal.

### 5. Kaggle Critical Minerals Supply Risk Index (page accessible)
- **Source**: [kaggle.com/datasets/philipdave/critical-minerals-supply-risk-index](https://www.kaggle.com/datasets/philipdave/critical-minerals-supply-risk-index)
- **Notes**: Kaggle dataset page loads (9.7 KB HTML), but bulk download requires Kaggle API authentication (`kaggle datasets download`). Pre-processed USGS-derived supply risk indices in CSV format.

## Not Accessible from Sandbox

| Source | Reason | Access Model |
|---|---|---|
| **DOE 2023 Critical Materials Strategy** | energy.gov blocked (404 from sandbox) | Open (government PDF) — accessible from browser |
| **BGS Supply Risk Index** | bgs.ac.uk main page loads but risk list URLs return 404 (site restructured) | Open — risk list published as PDF/web tables |
| **UN Comtrade** | API v1 requires authentication (401 Access Denied) | Open (API key required, free registration) |
| **World Bank WGI** | API v2 indicator codes changed/archived (`CC.EST`, `RL.EST`, `CC.PER.RNK` all return "indicator not found") | Open (direct CSV download at info.worldbank.org/governance/wgi works from browser) |
| **ESSENZ (TU Berlin)** | Page loads but characterization factor data is in published papers, not downloadable files | Open (academic publications) |
| **GeoPolRisk** | Academic method — data in published papers | Open (academic) |
| **Yale/Graedel** | Data in published supplementary materials | Open (academic) |
| **Ferro & Bonollo CIA** | Mendeley Data search API doesn't return the correct dataset (search term mismatch); dataset may need DOI-based lookup from browser | Open (Mendeley Data) |
| **Helbig et al. Superalloy SR** | Supplementary spreadsheets in journal paper | Open (academic supplementary) |

## Reproduction

```bash
# USGS MCS 2025 (all commodities)
python3 -c "
import urllib.request, json
url = 'https://www.sciencebase.gov/catalog/file/get/6793e234d34e72688d6b71e7'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    with open('usgs_salient_data.zip', 'wb') as f:
        f.write(resp.read())
"

# Mulukutla SupplyRiskAwareDesign
curl -L -o supply_risk_scores.csv https://raw.githubusercontent.com/mrinalinimulukutla/SupplyRiskAwareDesign/main/datafiles/supply_risk_scores.csv
curl -L -o elemental_properties.csv https://raw.githubusercontent.com/mrinalinimulukutla/SupplyRiskAwareDesign/main/datafiles/elemental_properties.csv

# Matminer
pip install matminer
python3 -c "
from matminer.datasets import load_dataset
df = load_dataset('elastic_tensor_2015')
al = df[df['formula'].str.startswith('Al')]
al.to_csv('matminer_elastic_al.csv', index=False)
"

# Kaggle (requires API key)
pip install kaggle
kaggle datasets download philipdave/critical-minerals-supply-risk-index
```
