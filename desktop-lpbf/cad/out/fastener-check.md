# Fasteners: our CadQuery parts against McMaster-Carr's CAD

Written by [`verify_fasteners.py`](../verify_fasteners.py). Volumes in mm³. *Light* is the shape used in the
model (plain shank at the major diameter), compared with McMaster's "3-D STEP simplified". *Detailed* adds the
thread as revolved rings with McMaster's axial profile (same volume per length as a helix), compared with
McMaster's full "3-D STEP". Helical inserts: light is the installed envelope (not comparable, so no figure);
detailed is the coil without its prong, against McMaster's coil *with* its prong, so it reads low by the prong.
McMaster's files are not committed; [`../fastener-cad-manifest.csv`](../fastener-cad-manifest.csv) lists them.

| Part | Kind | Description | Price | McMaster simplified | Ours, light | Δ light | McMaster full | Ours, detailed | Δ detailed | Extents match (light) |
|---|---|---|---|---|---|---|---|---|---|---|
| [92290A854](https://www.mcmaster.com/92290A854/) | shcs | 316 Stainless Steel Socket Head Screw, M2.5 x 0.45 mm Thread, 30 mm Long, Fully Threaded | $11.08 / pack of 10 | 181.341 | 181.344 | 0.0016 % | 148.865 | 150.174 | 0.879 % | yes |
| [92290A065](https://www.mcmaster.com/92290A065/) | shcs | 316 Stainless Steel Socket Head Screw, M2.5 x 0.45 mm Thread, 16 mm Long, Fully Threaded | $5.82 / pack of 10 | 112.620 | 112.622 | 0.0017 % | 96.044 | 96.136 | 0.096 % | yes |
| [92290A113](https://www.mcmaster.com/92290A113/) | shcs | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 8 mm Long, Fully Threaded | $14.30 / pack of 50 | 117.263 | 117.263 | 0.0003 % | 106.296 | 106.261 | -0.033 % | yes |
| [92290A115](https://www.mcmaster.com/92290A115/) | shcs | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 10 mm Long, Fully Threaded | $14.84 / pack of 50 | 131.399 | 131.400 | 0.0010 % | 117.662 | 117.586 | -0.065 % | yes |
| [92290A122](https://www.mcmaster.com/92290A122/) | shcs | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 20 mm Long, Fully Threaded | $17.00 / pack of 50 | 202.083 | 202.086 | 0.0014 % | 176.432 | 174.210 | -1.259 % | yes |
| [92290A124](https://www.mcmaster.com/92290A124/) | shcs | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 25 mm Long, Partially Threaded | $19.97 / pack of 50 | 236.387 | 236.391 | 0.0017 % | 211.836 | 211.417 | -0.198 % | yes |
| [92290A144](https://www.mcmaster.com/92290A144/) | shcs | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 10 mm Long, Fully Threaded | $17.81 / pack of 50 | 259.150 | 259.152 | 0.0009 % | 234.044 | 234.056 | 0.005 % | yes |
| [92290A148](https://www.mcmaster.com/92290A148/) | shcs | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 12 mm Long, Fully Threaded | $18.62 / pack of 50 | 284.284 | 284.285 | 0.0003 % | 254.431 | 253.814 | -0.242 % | yes |
| [92290A154](https://www.mcmaster.com/92290A154/) | shcs | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 16 mm Long, Fully Threaded | $19.02 / pack of 50 | 334.549 | 334.551 | 0.0006 % | 293.272 | 293.406 | 0.046 % | yes |
| [92290A168](https://www.mcmaster.com/92290A168/) | shcs | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 20 mm Long, Fully Threaded | $10.40 / pack of 25 | 384.814 | 384.816 | 0.0006 % | 334.764 | 333.586 | -0.352 % | yes |
| [92290A188](https://www.mcmaster.com/92290A188/) | shcs | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 50 mm Long, Partially Threaded | $7.49 / pack of 10 | 761.415 | 761.420 | 0.0007 % | 711.482 | 710.422 | -0.149 % | yes |
| [92290A228](https://www.mcmaster.com/92290A228/) | shcs | 316 Stainless Steel Socket Head Screw, M5 x 0.8 mm Thread, 12 mm Long, Fully Threaded | $11.47 / pack of 25 | 474.912 | 474.912 | 0.0001 % | 431.735 | 430.811 | -0.214 % | yes |
| [92290A242](https://www.mcmaster.com/92290A242/) | shcs | 316 Stainless Steel Socket Head Screw, M5 x 0.8 mm Thread, 20 mm Long, Fully Threaded | $14.30 / pack of 25 | 631.991 | 631.992 | 0.0001 % | 559.501 | 557.787 | -0.306 % | yes |
| [92290A252](https://www.mcmaster.com/92290A252/) | shcs | 316 Stainless Steel Socket Head Screw, M5 x 0.8 mm Thread, 25 mm Long, Fully Threaded | $15.11 / pack of 25 | 730.166 | 730.166 | 0.0001 % | 641.047 | 637.749 | -0.515 % | yes |
| [92290A321](https://www.mcmaster.com/92290A321/) | shcs | 316 Stainless Steel Socket Head Screw, M6 x 1 mm Thread, 16 mm Long, Fully Threaded | $15.30 / pack of 25 | 840.579 | 840.579 | 0.0000 % | 753.243 | 752.560 | -0.091 % | yes |
| [92290A326](https://www.mcmaster.com/92290A326/) | shcs | 316 Stainless Steel Socket Head Screw, M6 x 1 mm Thread, 20 mm Long, Fully Threaded | $15.79 / pack of 25 | 953.676 | 953.677 | 0.0000 % | 845.669 | 843.159 | -0.297 % | yes |
| [92290A330](https://www.mcmaster.com/92290A330/) | shcs | 316 Stainless Steel Socket Head Screw, M6 x 1 mm Thread, 25 mm Long, Fully Threaded | $17.54 / pack of 25 | 1095.048 | 1095.048 | 0.0000 % | 959.674 | 956.408 | -0.340 % | yes |
| [92290A334](https://www.mcmaster.com/92290A334/) | shcs | 316 Stainless Steel Socket Head Screw, M6 x 1 mm Thread, 35 mm Long, Partially Threaded | $9.75 / pack of 10 | 1369.629 | 1369.631 | 0.0002 % | 1239.537 | 1237.329 | -0.178 % | yes |
| [93395A204](https://www.mcmaster.com/93395A204/) | fhcs | 316 Stainless Steel Hex Drive Flat Head Screw, 90 Degree Countersink, M3 x 0.5 mm Thread, 10 mm Long | $15.65 / pack of 100 | 82.757 | 82.759 | 0.0015 % | 71.883 | 71.330 | -0.770 % | yes |
| [93395A254](https://www.mcmaster.com/93395A254/) | fhcs | 316 Stainless Steel Hex Drive Flat Head Screw, 90 Degree Countersink, M4 x 0.7 mm Thread, 10 mm Long | $19.97 / pack of 100 | 155.691 | 155.693 | 0.0009 % | 137.109 | 136.386 | -0.527 % | yes |
| [92029A140](https://www.mcmaster.com/92029A140/) | set | 316 Stainless Steel Cup-Point Set Screw, M4 x 0.7 mm Thread, 4 mm Long | $11.20 / pack of 50 | 37.380 | 37.381 | 0.0013 % | 29.445 | 29.217 | -0.774 % | yes |
| [92029A142](https://www.mcmaster.com/92029A142/) | set | 316 Stainless Steel Cup-Point Set Screw, M4 x 0.7 mm Thread, 6 mm Long | $12.38 / pack of 50 | 62.513 | 62.513 | 0.0013 % | 49.466 | 49.278 | -0.379 % | yes |
| [92029A152](https://www.mcmaster.com/92029A152/) | set | 316 Stainless Steel Cup-Point Set Screw, M4 x 0.7 mm Thread, 16 mm Long | $4.95 / pack of 10 | 188.175 | 188.177 | 0.0014 % | 149.479 | 148.600 | -0.588 % | yes |
| [92029A155](https://www.mcmaster.com/92029A155/) | set | 316 Stainless Steel Cup-Point Set Screw, M4 x 0.7 mm Thread, 20 mm Long | $6.18 / pack of 10 | 238.442 | 238.443 | 0.0004 % | 189.478 | 188.623 | -0.452 % | yes |
| [93600A686](https://www.mcmaster.com/93600A686/) | dowel | 316 Stainless Steel Dowel Pin, 6 mm Diameter, 20 mm Long (ISO 2338 m6) | $7.89 / pack of 5 | – | 558.473 | – | 558.473 | 558.473 | 0.000 % | – |
| [91732A767](https://www.mcmaster.com/91732A767/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M2.5 x 0.45 mm Thread Size, 3.8 mm Installed Length | $4.26 / pack of 10 | – | – | – | 17.051 | 16.403 | -3.798 % | – |
| [91732A647](https://www.mcmaster.com/91732A647/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M3 x 0.5 mm Thread Size, 4.5 mm Installed Length | $3.85 / pack of 10 | – | – | – | 27.301 | 26.268 | -3.784 % | – |
| [91732A649](https://www.mcmaster.com/91732A649/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M4 x 0.7 mm Thread Size, 4 mm Installed Length | $3.56 / pack of 10 | – | – | – | 35.648 | 34.519 | -3.166 % | – |
| [91732A656](https://www.mcmaster.com/91732A656/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M4 x 0.7 mm Thread Size, 6 mm Installed Length | $3.68 / pack of 10 | – | – | – | 56.161 | 53.998 | -3.852 % | – |
| [91732A261](https://www.mcmaster.com/91732A261/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M5 x 0.8 mm Thread Size, 7.5 mm Installed Length | $3.82 / pack of 10 | – | – | – | 98.160 | 95.150 | -3.066 % | – |
| [91732A262](https://www.mcmaster.com/91732A262/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M6 x 1 mm Thread Size, 9 mm Installed Length | $6.71 / pack of 10 | – | – | – | 151.274 | 146.079 | -3.434 % | – |
| [91732A782](https://www.mcmaster.com/91732A782/) | insert | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M6 x 1 mm Thread Size, 12 mm Installed Length | $4.56 / pack of 10 | – | – | – | 206.543 | 200.858 | -2.752 % | – |
| [95966A705](https://www.mcmaster.com/95966A705/) | captive | Socket Head Captive Panel Screw, M6 x 1 mm Thread, 20 mm Long (6 mm thread, 4.2 mm reduced shank) | $10.64 / each (1-24) | 711.317 | 711.319 | 0.0002 % | 677.941 | 685.459 | 1.109 % | yes |
| [91065A610](https://www.mcmaster.com/91065A610/) | retainer | Retainer for M6 x 1 mm Thread Size Captive Panel Screws, 18-8 Stainless Steel | $13.54 / pack of 25 | – | 9.289 | – | 9.267 | 9.289 | 0.242 % | – |
| [97125K111](https://www.mcmaster.com/97125K111/) | disc | Extreme-Temperature Belleville Disc Spring, 718 Nickel, for 0.138" Shaft, 0.142" ID, 0.281" OD, 0.021" Thick | $1.69 / each | – | 15.212 | – | 15.212 | 15.212 | -0.000 % | – |
| [9713K54](https://www.mcmaster.com/9713K54/) | disc | Belleville Disc Spring, 302 Stainless Steel, for 1/8" Shaft, 0.125" ID, 0.25" OD, 0.013" Thick | $11.81 / pack of 12 | – | 7.953 | – | 8.042 | 7.953 | -1.106 % | – |
