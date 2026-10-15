# Database Samples

Small data subsets downloaded from alloy databases to verify access and illustrate data formats. Each file demonstrates what kind of data is available from the corresponding source.

## Successfully Accessed Databases

### Open-Access Computational Repositories (API)

| Source | Files | Description |
| :--- | :--- | :--- |
| **AFLOW/AFLOWLIB** | `aflow_al_alloys.json`, `aflow_mg_alloys.json`, `aflow_al_mg_binary.json` | 10 entries each via AFLUX REST API. Contains compound name, AUID, space group, Pearson symbol, species, formation enthalpy. No API key required. |
| **OQMD** | `oqmd_al.json`, `oqmd_mg.json`, `oqmd_al_mg.json` | 10 entries each via REST API. Contains entry ID, composition, formation energy (delta_e), stability, band gap. No API key required. |
| **NOMAD** | `nomad_al.json` | 10 entries via POST query API. Contains entry ID, chemical formula, structural type. No API key required. |
| **JARVIS (NIST)** | `jarvis_al.json`, `jarvis_mg.json` | 10 entries each via `jarvis-tools` Python package (auto-downloads 76K-entry DFT-3D dataset from Figshare). Contains JID, formula, formation energy, energy above hull, band gap, bulk/shear modulus, space group, density. |

### Open Research Datasets (Direct Download)

| Source | Files | Description |
| :--- | :--- | :--- |
| **FatigueData-CMA2022** (Zhang 2023) | `fatigue_cma2022_sample.xlsx` | Full 762 KB Excel dataset from Figshare (CC BY 4.0). Contains 272 fatigue datasets (S-N, ε-N, da/dN-ΔK) compiled from 1,249 articles. |
| **LPBF Relative Density** (Barrionuevo 2025) | `lpbf_barrionuevo_dataset.xlsx` | Full 222 KB Excel dataset from Harvard Dataverse. 1,579 samples across 6 alloys (316L, IN718, Ti6Al4V, CuCrZr, AlSi10Mg, 18Ni300) with 10 processing parameters. |
| **HCF AlSi10Mg/316L** (Zenodo) | `zenodo_hcf_Data.xlsx` | 22 KB Excel dataset of high-cycle fatigue data for SLM 316L and AlSi10Mg. |
| **AlloyML** (Mangos & Birbilis) | `alloyml_dos_Template.csv`, `alloyml_mechanical_Template.csv` | Input templates from GitHub (joseph42440/AlloyML). Training data (516 DoS + 1,154 mechanical property entries) not included in the repo — referenced from Dropbox in the paper. |

### CALPHAD / Thermodynamic (Open-Source)

| Source | Files | Description |
| :--- | :--- | :--- |
| **pycalphad** | `pycalphad_al_mg.json`, `pycalphad_cu_mg.json`, `pycalphad_alcocrni_hea.json`, `pycalphad_example_db.json` | Summaries of built-in test TDB databases (35 TDB files ship with pycalphad 0.11.1). Al-Mg (Zhong), Cu-Mg, Al-Co-Cr-Ni HEA, Al-Ni systems. Phase names, elements, sample equilibrium calculations. |

### Specialized (Template/Schema)

| Source | Files | Description |
| :--- | :--- | :--- |
| **ULTERA** (PhasesResearchLab) | `ultera_template_v4.xlsx`, `ultera_template_v4_DatasetExample.xlsx` | Contribution template and example from GitHub. Shows the schema used for HEA data ingestion. Actual database access requires contacting PhasesResearchLab. |

## Databases Tested But Not Accessible (from sandbox)

| Database | Status | Notes |
| :--- | :--- | :--- |
| **Materials Project** | ❌ API key required (401) | Free API key available at materialsproject.org after registration |
| **MatWeb** | ❌ Blocked (403) | Blocks automated access; manual web browsing only |
| **MatNavi/NIMS** | ❌ Network blocked | Registration required; web interface accessible from normal browsers |
| **Materials Commons** | ❌ API endpoints not found (404) | Website loads but REST API endpoints have changed; web UI browsing works |
| **Knovel** | ❌ Login required | Proprietary; University of Utah has institutional subscription |
| **Total Materia** | ❌ Login required | Proprietary subscription |
| **ASM International** | ❌ Login required | Proprietary subscription |
| **SpringerMaterials** | ❌ No public API (404) | Proprietary; via institutional library subscription |
| **Citrine/Citrination** | ❌ API key required (403) | Enterprise platform; free tier may be available |
| **MMPDS** | ❌ Proprietary | Subscription required; no API |
| **Granta/ANSYS EduPack** | ❌ Desktop software | Educational license via university; not web-accessible |
| **Thermo-Calc** | ❌ Commercial license | Requires purchased license + TC-Python for API access |
| **JMatPro / Pandat** | ❌ Commercial license | Desktop software with batch mode |

## How to Reproduce

```bash
# AFLOW (no key needed)
curl "http://aflow.org/API/aflux/?species(Al),nspecies(1),enthalpy_formation_atom,\$paging(1,10),format(json)"

# OQMD (no key needed)
curl "http://oqmd.org/oqmdapi/formationenergy?composition=Al&limit=10&format=json"

# NOMAD (no key needed)
curl -X POST "https://nomad-lab.eu/prod/v1/api/v1/entries/query" \
  -H "Content-Type: application/json" \
  -d '{"query":{"results.material.elements":{"all":["Al"]}},"pagination":{"page_size":10}}'

# JARVIS (via Python)
pip install jarvis-tools
python -c "from jarvis.db.figshare import data; d=data('dft_3d'); print(len(d))"

# Materials Project (requires free API key)
pip install mp-api
# Register at materialsproject.org, then:
# from mp_api.client import MPRester
# with MPRester("YOUR_API_KEY") as mpr: docs = mpr.summary.search(elements=["Al"], num_elements=(1,3))

# pycalphad (open-source CALPHAD)
pip install pycalphad
python -c "import pycalphad as pc; db=pc.Database('Al-Mg_Zhong.tdb'); print(db.phases.keys())"
```
