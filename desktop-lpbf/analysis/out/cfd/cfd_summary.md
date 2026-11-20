# Chamber cross-flow CFD: key numbers per case

Written by `analysis/cfd/post.py` from `cfd.json`. Speeds in m/s (horizontal speed on discs centred on the plate), shear in Pa, pressures in Pa above the outlet flange. 'fix' = screens in both slots, 35 mm outlet channel with a KF-40 boot, 100 x 4 mm upper slot under the lid (see gas-flow.md).

| | fine | coarse | fix140 | fix200 |
|---|---|---|---|---|
| cells / iterations | 427k / 600 | 173k / 1500 | 175k / 700 | 175k / 800 |
| bed slot + upper slot flow (L/min) | 115 + 0 | 115 + 0 | 140 + 30 | 200 + 40 |
| speed at 1 mm over Ø25: mean (min-max), CoV | 1.54 (1.34-1.78), CoV 8 % | 1.60 (1.43-1.81), CoV 6 % | 1.43 (1.38-1.50), CoV 2 % | 2.25 (2.19-2.31), CoV 1 % |
| speed at 1 mm over Ø50: mean (min-max), CoV | 1.54 (1.15-2.04), CoV 16 % | 1.60 (1.27-2.04), CoV 13 % | 1.38 (1.21-1.55), CoV 6 % | 2.20 (2.03-2.35), CoV 4 % |
| speed at 1 mm over Ø75: mean (min-max), CoV | 1.53 (0.96-2.32), CoV 24 % | 1.61 (1.12-2.29), CoV 19 % | 1.32 (1.05-1.59), CoV 10 % | 2.12 (1.78-2.37), CoV 7 % |
| speed at 3 mm over Ø25: mean (min-max), CoV | 1.53 (1.42-1.67), CoV 5 % | 1.45 (1.36-1.57), CoV 4 % | 2.13 (2.08-2.20), CoV 2 % | 3.08 (3.01-3.16), CoV 1 % |
| speed at 3 mm over Ø50: mean (min-max), CoV | 1.53 (1.31-1.82), CoV 9 % | 1.45 (1.26-1.70), CoV 8 % | 2.07 (1.90-2.25), CoV 4 % | 3.00 (2.78-3.23), CoV 4 % |
| speed at 3 mm over Ø75: mean (min-max), CoV | 1.52 (1.20-1.99), CoV 14 % | 1.46 (1.17-1.87), CoV 12 % | 2.00 (1.75-2.29), CoV 7 % | 2.91 (2.58-3.28), CoV 6 % |
| speed at 10 mm over Ø25: mean (min-max), CoV | 0.48 (0.41-0.54), CoV 8 % | 0.42 (0.33-0.48), CoV 9 % | 1.73 (1.69-1.75), CoV 1 % | 2.48 (2.41-2.52), CoV 1 % |
| speed at 10 mm over Ø50: mean (min-max), CoV | 0.48 (0.30-0.57), CoV 15 % | 0.42 (0.24-0.54), CoV 18 % | 1.69 (1.57-1.75), CoV 3 % | 2.39 (2.18-2.52), CoV 4 % |
| speed at 10 mm over Ø75: mean (min-max), CoV | 0.48 (0.18-0.64), CoV 24 % | 0.42 (0.12-0.58), CoV 28 % | 1.64 (1.51-1.75), CoV 4 % | 2.31 (2.11-2.52), CoV 5 % |
| share of Ø75 >= 2.5 m/s at 3 mm | 0 % | 0 % | 0 % | 100 % |
| inlet slot: min / max / middle-third share | 1.41 / 2.83 / 43 % | 1.05 / 2.82 / 45 % | 1.75 / 2.55 / 35 % | 2.51 / 3.64 / 35 % |
| outlet slot: min / max / right-half share | -0.16 / 8.07 / 85 % | -0.09 / 7.14 / 84 % | 2.48 / 3.35 / 53 % | 3.50 / 4.72 / 53 % |
| pressure drop flange to flange (Pa) | 473 | 467 | 294 | 589 |
| bed shear over Ø75: mean / max (Pa) | 0.067 / 0.114 | 0.063 / 0.098 | 0.044 / 0.055 | 0.081 / 0.092 |
| highest shear on the floor (Pa) | 0.34 | 0.29 | 0.16 | 0.26 |
| under the slide (z 121): mean speed, mean Uy | 0.22, +0.17 | 0.16, +0.10 | 0.29, -0.29 | 0.53, -0.52 |
| gas over the plate at z 30-120 flowing toward the inlet | 91 % | 84 % | 27 % | 23 % |
| condensate from 1-10 mm: out in 12 s / median time (s) | 95 % / 0.13 | 98 % / 0.12 | 88 % / 0.09 | 72 % / 0.13 |
| condensate from 1-10 mm: near the window / into the slide recess | 2.1 % / 0.5 % | 1.2 % / 0.2 % | 3.2 % / 0.1 % | 3.7 % / 0.1 % |
| condensate from 10-30 mm: out in 12 s / median time (s) | 91 % / 0.37 | 93 % / 0.35 | 90 % / 1.41 | 82 % / 1.70 |
| condensate from 10-30 mm: near the window / into the slide recess | 8.1 % / 1.9 % | 5.9 % / 0.9 % | 12.2 % / 0.5 % | 13.3 % / 1.1 % |
| spatter 50 um: back on Ø75 / lid / slide footprint | 10 / 0 / 0 % | 11 / 0 / 0 % | 0 / 0 / 0 % | 0 / 0 / 0 % |
| spatter 100 um: back on Ø75 / lid / slide footprint | 17 / 6 / 2 % | 18 / 6 / 2 % | 9 / 7 / 2 % | 2 / 6 / 2 % |
| spatter 150 um: back on Ø75 / lid / slide footprint | 7 / 32 / 10 % | 7 / 32 / 10 % | 6 / 33 / 10 % | 3 / 31 / 10 % |

Shao & Lu (2000) entrainment threshold for loose AlSi10Mg spheres in argon (Pa):

| d | γ = 1.65e-4 N/m | 3e-4 | 5e-4 |
|---|---|---|---|
| 20 um | 0.108 | 0.191 | 0.314 |
| 40 um | 0.064 | 0.105 | 0.167 |
| 63 um | 0.053 | 0.079 | 0.118 |
