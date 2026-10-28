# Particle size and shape summary (sem_psd.py 1.0)

- Fields: 3.2nA_001, 3.2nA_002, 3.2nA_004, not annotated, spherical, spherical_001, spherical_002, spherical_003, spherical_004
- Area analysed: 27.76 mm² (union of fields, overlaps counted once)
- Regions segmented: 8,828; counted: **5,937**; excluded: 928 touching the frame, 1,682 in a patch owned by another field, 281 below 10 px

## Size (equivalent circle diameter, µm)

| Weighting | D10 | D50 | D90 | Span |
|---|---|---|---|---|
| number | 34.8 (34.5–35.3; fields 34.4–35.4) | 46.9 (46.6–47.2; fields 46.1–48.3) | 71.5 (69.5–73.7; fields 64.6–102.5) | 0.78 |
| volume | 45.8 (45.1–46.6; fields 42.1–54.2) | 103.7 (91.8–116.3; fields 60.3–156.8) | 208.5 (188.6–289.8; fields 132.4–275.1) | 1.57 |

95 % intervals: particle bootstrap, then field (cluster) bootstrap.

## Shares

| Range | By number | By volume |
|---|---|---|
| 50–200 µm | 37.6 % (36.4–38.8) | 69.8 % (63.4–75.8) |
| < 20 µm | 2.1 % (1.7–2.5) | 0.0 % (0.0–0.0) |
| > 200 µm | 0.3 % (0.1–0.4) | 13.5 % (6.5–21.4) |

## Shape (ISO 9276-6), 5,858 particles ≥ 20 px

| Descriptor | Median | IQR | P10 | P90 |
|---|---|---|---|---|
| circularity | 0.993 | 0.985–0.998 | 0.965 | 1.000 |
| form_factor | 0.987 | 0.970–0.995 | 0.932 | 1.000 |
| aspect_ratio | 0.946 | 0.921–0.960 | 0.852 | 0.969 |
| ellipse_ratio | 0.968 | 0.946–0.981 | 0.879 | 0.989 |
| solidity | 0.982 | 0.976–0.985 | 0.965 | 0.987 |
| convexity | 0.998 | 0.994–1.000 | 0.987 | 1.000 |
| aspect_ratio_norm | 0.965 | 0.940–0.978 | 0.871 | 0.987 |
| solidity_norm | 0.997 | 0.992–0.999 | 0.981 | 1.001 |

Particles of at least 3,000 px only (n = 3,667): form factor median 0.987 (IQR 0.971–0.995), circularity 0.994, aspect ratio 0.952, solidity 0.983.

circularity = 2√(πA)/P (ISO 9276-6 square-root form); form_factor = 4πA/P² (often also called circularity); P = Crofton perimeter; aspect_ratio = Feret min / Feret max; ellipse_ratio = minor / major axis of the moment ellipse; solidity = A / convex-hull area; convexity = convex-hull perimeter / P; *_norm = divided by the value for an ideal digitised disc of the same size (pixelation_bias.csv).

Flags among counted particles: {'none': 5442, 'irregular': 305, 'agglomerate_or_elongated': 178, 'oversize': 9, 'agglomerate_or_elongated+oversize': 2, 'irregular+oversize': 1}

