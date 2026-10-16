# EDAX Smart Quant EDS Mapping Reports — Feedstock Characterization

Preliminary SEM/EDS mapping on \flaime{} baseline feedstocks (2026-04-21),
captured on the BYU EDAX TEAM system (15 kV, ~500 s live time).

Source: [byu-vcl#49, comment 4292356704](https://github.com/vertical-cloud-lab/byu-vcl/issues/49#issuecomment-4292356704)
(Gage Erickson). PDF reports are authoritative; PNGs are per-page rasterizations at 150 dpi.

## Samples

| File | Sample | Mag | Key finding |
|---|---|---|---|
| `Si-100-Mapping.pdf` | Si (100-mesh, as-received) | 500× | Dominant Si (32 wt% excluding C/O); trace Fe (0.08 wt%) |
| `Si-40-Mapping.pdf`  | Si (40-mesh, as-received) | 2000× | Dominant Si (94 wt%); **Fe 1.1 wt%, Ca 0.4 wt%, Al 1.5 wt% contamination** (possible grinding-media / bin cross-contamination) |
| `AlSi10Mg-40-Micron-Mapping.pdf` | AlSi10Mg powder (40 µm, reference feedstock) | 1000× | Al 58 + Si 5 + Mg 0.9 wt% matrix consistent with nominal AlSi10Mg; C/O from tape/surface oxide |

## Sum-spectrum quantification (eZAF Smart Quant, matrix-only row)

### Si-100 (area 1, whole field)
| Element | Wt % | At % |
|---|---|---|
| C  | 63.48 | 78.96 |
| O  |  4.07 |  3.80 |
| Si | 32.37 | 17.22 |
| Fe |  0.08 |  0.02 |

### Si-40 (area 2, whole field)
| Element | Wt % | At % |
|---|---|---|
| C  |  2.22 |  5.04 |
| O  |  0.70 |  1.20 |
| Al |  1.49 |  1.51 |
| Si | 94.10 | 91.46 |
| Ca |  0.36 |  0.24 |
| Fe |  1.13 |  0.55 |

### AlSi10Mg 40 µm (area 3, whole field)
| Element | Wt % | At % |
|---|---|---|
| C  | 34.41 | 53.77 |
| O  |  1.44 |  1.69 |
| Mg |  0.88 |  0.68 |
| Al | 58.22 | 40.49 |
| Si |  5.05 |  3.38 |

Note: C and O signal comes from the carbon tape and native surface oxide;
normalizing to the metal matrix only gives Al 90.8 / Si 7.9 / Mg 1.4 wt% for
AlSi10Mg, within nominal spec (9–11 wt% Si, 0.2–0.45 wt% Mg).

## Suggested proposal uses

1. **Fig. 1 (atomization-process-annotated):** the per-element ROI maps
   already baked into the composite could be refreshed with these new
   (fuller) quant tables; the AlSi10Mg map is the reference.
2. **App. 2 (Facilities) / App. 3 (Equipment):** cite as evidence that
   the BYU Microscopy Center SEM/EDS workflow is operational on
   \flaime{} feedstocks (Gage Erickson trained).
3. **App. 3 / budget (characterization recharge line):** the Si-40 Fe+Ca+Al
   contamination demonstrates the working QC pipeline and justifies the
   "every-tenth-composition ICP-MS provenance audit" + per-lot SEM/EDS
   pre-atomization screen (app-budget line item).
