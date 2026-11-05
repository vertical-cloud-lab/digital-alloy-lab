# eagar-tsai inputs for AlSi10Mg (issue #235)

Two Edison `LITERATURE_HIGH` (`job-futurehouse-paperqa3-high`) queries, submitted 2026-11-04, asking
for the eight inputs of [ArroyaveLab/eagar-tsai](https://github.com/ArroyaveLab/eagar-tsai)
(`BeamParameters` and `MaterialProperties`) for AlSi10Mg on an Aconity MIDI, followed by an eagar-tsai
0.6.0 run with the values.

| File | What it is |
|---|---|
| [`beam-parameter-ranges.md`](beam-parameter-ranges.md) | Edison report, task `69989f43-9df7-443e-aac4-438c040a3ea6` |
| [`material-properties.md`](material-properties.md) | Edison report, task `c678f8a7-903a-427c-a766-6706fcea069a` |
| `raw/*-task-verbose.json` | Full verbose task dumps (corresponding-author emails redacted) |
| `alsi10mg-temperature-field.png`, `alsi10mg-sensitivity.csv`, `alsi10mg-printability-map.png` | eagar-tsai run |
| [`../../scripts/edison_eagar_tsai_alsi10mg.py`](../../scripts/edison_eagar_tsai_alsi10mg.py) | Prompts; submit / wait / fetch |
| [`../../scripts/eagar_tsai_alsi10mg.py`](../../scripts/eagar_tsai_alsi10mg.py) | eagar-tsai run |

**Beam-diameter convention.** eagar-tsai's `beam_diameter` is **2σ** (σ = Gaussian standard deviation). That is
**half** the 1/e² (D4σ) spot diameter that machine datasheets quote, and about 0.85 × FWHM.

## Beam / process inputs

| eagar-tsai input | Use | Range | Sources |
|---|---|---|---|
| `beam_diameter` (2σ) | **40e-6 m**: the MIDI's 80 µm focused spot, assumed 1/e², halved | 25–250 µm (50–500 µm 1/e², i.e. focused across machines up to the MIDI's defocus limit) | MIDI configuration with 400 W, 1070 nm and an 80–500 µm spot: Kantonen 2023 thesis (another site's MIDI); machine comparison: [10.1007/s44245-024-00073-4](https://doi.org/10.1007/s44245-024-00073-4); an explicit 1/e² convention: [10.1002/adem.201900185](https://doi.org/10.1002/adem.201900185) |
| `power` | **300 W** (dense window 200–370 W) | map sweep 50–400 W | [10.1016/j.jmatprotec.2015.11.016](https://doi.org/10.1016/j.jmatprotec.2015.11.016), [10.3390/jmmp6050112](https://doi.org/10.3390/jmmp6050112), [10.1016/j.matdes.2019.108018](https://doi.org/10.1016/j.matdes.2019.108018), [10.1007/s44245-024-00073-4](https://doi.org/10.1007/s44245-024-00073-4) |
| `velocity` | **1.0 m/s** (dense window 0.8–1.3 m/s) | map sweep 0.1–2.5 m/s | same as power |
| `absorptivity` | **0.25** (sensitivity 0.15 and 0.35) | 0.05 (polished flat Al) to about 0.7 (keyhole) | [10.1364/AO.55.006496](https://doi.org/10.1364/AO.55.006496) (Al powder 0.53, oxidised bulk 0.20), [10.1016/j.apmt.2017.08.006](https://doi.org/10.1016/j.apmt.2017.08.006), [10.1007/s00161-026-01516-x](https://doi.org/10.1007/s00161-026-01516-x) (**Eagar–Tsai back-calibrated on AlSi10Mg single tracks: 0.22 for d50 = 44 µm powder, 0.11–0.38 across size fractions**), [10.1002/adem.201900185](https://doi.org/10.1002/adem.201900185) (keyhole saturation near 0.70) |

## Material inputs

| eagar-tsai input | Use | Range | Sources |
|---|---|---|---|
| `liquidus_temperature` | **867 K** (594 °C); solidus 831 K | 860–870 K | [10.2139/ssrn.3490412](https://doi.org/10.2139/ssrn.3490412), [10.3390/modelling6040135](https://doi.org/10.3390/modelling6040135); 870 K in [10.48550/arXiv.2003.09757](https://doi.org/10.48550/arXiv.2003.09757) |
| `thermal_conductivity` | **110 W/(m·K)**, a solid value near the solidus (Patel & Vlasea use 113) | 63 (liquid at the liquidus) to 155; as-built at room temperature 103–136, stress-relieved 168–173 | [10.1016/j.addma.2020.101214](https://doi.org/10.1016/j.addma.2020.101214), [10.1108/rpj-09-2022-0290](https://doi.org/10.1108/rpj-09-2022-0290), [10.1007/s11665-020-05192-z](https://doi.org/10.1007/s11665-020-05192-z), [10.1038/s41598-021-85047-2](https://doi.org/10.1038/s41598-021-85047-2), [10.2351/1.5104318](https://doi.org/10.2351/1.5104318), [10.3390/modelling6040135](https://doi.org/10.3390/modelling6040135) |
| `density` | **2650 kg/m³** (solid), or 2500 for the liquid at the liquidus | 2500–2700 | [10.3390/modelling6040135](https://doi.org/10.3390/modelling6040135) (liquid 2500), [10.2139/ssrn.3490412](https://doi.org/10.2139/ssrn.3490412) and [10.2351/1.5104318](https://doi.org/10.2351/1.5104318) (2670), [10.3390/ma16144920](https://doi.org/10.3390/ma16144920) (2700 theoretical; 2620–2715 measured) |
| `specific_heat` | **1040 J/(kg·K)**: the liquid value at the liquidus, 2.6 MJ/(m³·K) ÷ 2500 kg/m³ | 920–1200; 1365 as an effective cp that includes latent heat | [10.3390/modelling6040135](https://doi.org/10.3390/modelling6040135), [10.1007/s11665-023-08502-3](https://doi.org/10.1007/s11665-023-08502-3), [10.2351/1.5104318](https://doi.org/10.2351/1.5104318) (739–922 for the solid, 20–400 °C) |

## Problems in the Edison reports

1. **Thermal-conductivity arithmetic.** The report derives a liquid value of 53 W/(m·K) from Pelevin et al. Their
   formula gives (1.88e-5 + 6.43e-9 × 867) m²/s × 2.6e6 J/(m³·K) = **63 W/(m·K)**.
2. **Density is inconsistent.** The summary table recommends 2500 kg/m³ (liquid); the closing recommendation
   says 2650 kg/m³ (solid). The run below tries both.
3. **Specific-heat range** is 920–1200 in the text and 920–1040 in the table. Patel & Vlasea's 565 J/(kg·K) looks too low for Al
   near its melting point; Edison flags it too.
4. **Machine data come from a thesis on a different MIDI** (400 W, 80–500 µm). Check our University of Utah
   machine's laser power and spot size, and whether the spot is quoted as 1/e².
5. **Claims without citations:** Aconity scan speeds of 5–8 m/s; EOS defaults of 370 W, 1300 mm/s and 0.19 mm hatch; spot
   sizes for the Concept Laser, SLM and Renishaw machines; Mg evaporation above about 1100 °C; and a Drude
   absorptivity of 0.08–0.15 for Al. The claim of a TCAL6 Scheil liquidus near 867 K cites papers that probably do not report one, so it is weakly
   supported. Thermo-Calc or pycalphad can check it.

## eagar-tsai run (0.6.0, `scripts/eagar_tsai_alsi10mg.py`)

The nominal case uses 300 W, 1.0 m/s, `beam_diameter` 40 µm, A = 0.25, 867 K, 110 W/(m·K), 2650 kg/m³ and
1040 J/(kg·K). It gives **L = 248 µm, W = 180 µm, D = 84 µm**. With every property taken for the liquid at the
liquidus (k = 63, ρ = 2500) the pool grows to L = 386, W = 204, D = 98 µm. The full one-at-a-time table is in
`alsi10mg-sensitivity.csv`.

- Absorptivity matters most (0.15 → 0.35: W 132 → 220 µm, D 56 → 104 µm), followed by k (63 → 155: W 200 → 160, D 94 → 74) and
  power. The liquidus (860–870 K) and density barely change the result.
- **The beam-convention trap.** Entering the 80 µm 1/e² spot instead of 40 µm gives W = 196 and D = 74 µm, versus 180 and 84. The peak
  temperature drops from 6053 K to 2841 K.
- Peak temperatures of 4000–10000 K, far above aluminium's boiling point (about 2740 K), show that the
  conduction-only model is outside its validity range at these settings. Vapour, recoil and keyhole physics are not in it.
- **The printability map has no defect-free region** with the package's default criteria (Sheikh et al. 2024). Its
  KH1 test (W/D ≤ 2.5) labels nearly everything above about 100–180 W as keyhole, because aluminium's high diffusivity
  gives W/D ≈ 2 at the usual dense-part settings (nominal 180/84 = 2.1). AlSi10Mg prints dense there, so the
  keyhole threshold needs calibrating against our single-track cross-sections before the map can be used for Al.
  The layer thickness (30 µm) and hatch spacing (190 µm) are assumed EOS-like defaults, not values sourced from Edison.
