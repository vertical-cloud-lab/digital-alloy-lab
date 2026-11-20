# Build plate materials: how far the plate-to-bore gap closes at build start (CalculiX, axisymmetric)

Asked on [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266): *"A 0.10 mm plate clearance seizes on Ø75 ... Cold clearances are now 0.10 / 0.15 / 0.20 mm, which leaves 51–96 µm hot. Is there a different material with a lower thermal expansion coefficient that would make sense to use?"*

`analysis/thermal_module.py plates` re-runs the steady build-start case of [`thermal.md`](thermal.md) once per candidate plate: plate top at the powder plane (z_p 0), plate top centre held at 200 °C by the same secant on heater power, chamber 25 °C, powder on the plate (ε 0.5), argon in the gaps, today's cold radial clearances (S25 / M50 / L75 = 0.10 / 0.15 / 0.20 mm). Only the plate changes: its own conductivity in the FEA (temperature-dependent where the datasheet gives it) and its own expansion in the clearance. The heater block stays 6061 and the bore 316L.

Closing = R_plate · ᾱ_plate · (T_plate − 20) − R_bore · ᾱ_bore · (T_bore − 20). T_plate and T_bore are the FEA's area-mean temperatures of the plate and of the spigot ring beside it; ᾱ is each material's mean CTE from room temperature to that temperature, interpolated in its datasheet's table (316L bore: 16.0 µm/m·K to 100 °C). Hot clearance = cold clearance − closing. **Least cold clearance** = 25 µm + closing: the cold radial clearance that still leaves 25 µm at steady build start. "≥" marks plates whose datasheet gives the CTE only to 100 °C; the value there is held, which under-states the closing.

## Tier A: 200 °C plate, build start (the worst case)

| Plate | Mean CTE, 20 → 200 °C (µm/m·K) | Closing, S25 / M50 / L75 (µm) | Hot clearance at today's 100 / 150 / 200 µm cold (µm) | Least cold clearance, S25 / M50 / L75 (µm) | Heater, S25 / M50 / L75 (W) | Plate centre − edge (°C) | Block max, S25 / M50 / L75 (°C) |
|---|---|---|---|---|---|---|---|
| 6061-T6 (today) | 24.4 | 51 / 98 / 142 | 49 / 52 / 58 | **76 / 123 / 167** | 44 / 72 / 97 | 1–2 | 221 / 206 / 204 |
| 4032-T6/T86 | ≥ 19.4 | ≥ 39 / 75 / 108 | ≤ 61 / 75 / 92 | **≥ 64 / 100 / 133** | 44 / 72 / 97 | 1–2 | 222 / 206 / 204 |
| AlSi10Mg, printed, stress-relieved | ≥ 20.9 | ≥ 43 / 82 / 118 | ≤ 57 / 68 / 82 | **≥ 68 / 107 / 143** | 44 / 72 / 97 | 1–2 | 221 / 206 / 204 |
| Ti-6Al-4V (Grade 5) | 9.0 | 16 / 28 / 37 | 84 / 122 / 163 | **41 / 53 / 62** | 45 / 70 / 95 | 16–19 | 241 / 210 / 206 |
| 17-4 PH, H1150 | 12.4 | 23 / 43 / 60 | 77 / 107 / 140 | **48 / 68 / 85** | 44 / 71 / 95 | 10–11 | 231 / 207 / 204 |
| 430 ferritic stainless | 10.7 | 19 / 35 / 49 | 81 / 115 / 151 | **44 / 60 / 74** | 44 / 71 / 96 | 7–8 | 228 / 207 / 204 |
| 410 stainless, annealed | 10.6 | 19 / 35 / 48 | 81 / 115 / 152 | **44 / 60 / 73** | 44 / 71 / 96 | 7–8 | 228 / 207 / 204 |
| 316L | 16.1 | 32 / 59 / 85 | 68 / 91 / 115 | **57 / 84 / 110** | 44 / 71 / 95 | 10–11 | 231 / 208 / 204 |
| Invar 36 (a bound only) | 3.1 | 2 / 1 / -3 | 98 / 149 / 203 | **27 / 26 / 22** | 45 / 70 / 95 | 15–17 | 239 / 209 / 206 |

**Bore option**, 6061 spigot, tube and flange round the 6061 plate (M50 / L75): aluminium carries the heat to the floor, so the bore ring runs at 36 / 39 °C instead of 52 / 59 °C and grows no more than the 316L one: closing 101 / 149 µm (316L bore: 98 / 142), and the heater needs 81 / 107 W instead of 72 / 97 W.

## Tier B reserve: M50 at 500 °C, 0.20 mm cold (316L head and flange band water-cooled, as in thermal.md)

| Plate | Mean CTE, 20 → 500 °C (µm/m·K) | Closing (µm) | Hot clearance at 200 µm cold (µm) | Least cold clearance (µm) | Heater (W) | Plate centre − edge (°C) | Block max (°C) | At 500 °C |
|---|---|---|---|---|---|---|---|---|
| 6061-T6 (today) | ≥ 25.2 | ≥ 281 | ≤ -81 | **≥ 306** | 235 | 5 | 520 | solidus 582 °C |
| 4032-T6/T86 | ≥ 19.4 | ≥ 211 | ≤ -11 | **≥ 236** | 235 | 6 | 520 | solidus 530 °C; strength listed to 180 °C |
| Ti-6Al-4V (Grade 5) | 9.5 | 91 | 109 | **116** | 230 | 38 | 529 | properties held to ~350 °C |
| 17-4 PH, H1150 | ≥ 13.1 | ≥ 135 | ≤ 65 | **≥ 160** | 231 | 26 | 525 | good properties to 316 °C; above that it loses toughness (re-age 4 h at 621 °C) |
| 430 ferritic stainless | 11.3 | 113 | 87 | **138** | 232 | 23 | 524 | embrittles above ~340 °C (worst ~475 °C) |
| 316L | 17.2 | 184 | 16 | **209** | 231 | 27 | 525 | – |

## The plates: properties used and what they suit

| Plate | k at 200 °C (W/m·K) | Mean CTE from room temperature (°C: µm/m·K) | Density (kg/m³) | Limit | Powders it suits | Sources |
|---|---|---|---|---|---|---|
| 6061-T6 (today) | 167.0 (one value) | 100: 23.6, 300: 25.2 | 2700 | solidus 582 °C | Al alloys | [1][2] |
| 4032-T6/T86 | 138.0 (one value) | 100: 19.4 | 2680 | solidus 530 °C; strength listed to 180 °C | Al alloys (Al-Si family, as AlSi10Mg) | [3][4] |
| AlSi10Mg, printed, stress-relieved | 165.0 (one value) | 100: 20.9 | 2680 | melting from 557 °C | AlSi10Mg (same alloy) | [5] |
| Ti-6Al-4V (Grade 5) | 9.0 | 100: 9, 200: 9, 425: 9.4, 650: 9.7 | 4420 | properties held to ~350 °C | Ti alloys | [6][7] |
| 17-4 PH, H1150 | 18.6 | 93: 11.9, 204: 12.4, 316: 12.8, 427: 13, 482: 13.1 | 7820 | good properties to 316 °C; above that it loses toughness (re-age 4 h at 621 °C) | steels, Ni alloys | [8] |
| 430 ferritic stainless | 26.1 (one value) | 100: 10.4, 315: 11, 540: 11.4 | 7700 | embrittles above ~340 °C (worst ~475 °C) | steels, Ni alloys | [9][10] |
| 410 stainless, annealed | 25.8 | 100: 9.9, 315: 11.4, 538: 11.6 | 7700 | not for use at 400–580 °C | steels, Ni alloys (the thick-stock stand-in for 430) | [11] |
| 316L | 17.5 | 100: 16, 315: 16.2, 538: 17.5, 649: 18.5 | 8030 | – | 316L and other steels, Ni alloys | [12] |
| Invar 36 (a bound only) | 10.5 (one value) | 93: 1.3, 149: 2.11, 260: 4.18, 371: 7.6 | 8055 | Curie point 279 °C: the CTE climbs above it | – (bound) | [13] |

## What this means

1. **Today's 6061 plate works at today's clearances.** With 6061's mean CTE to 200 °C (24.4 µm/m·K, against the 20–100 °C value of 23.6 that thermal.md used; 316L bore 16.0 against 16.5) the hot gap at build start is 49 / 52 / 58 µm (S25 / M50 / L75), 2 / 4 / 6 µm less than thermal.md reports, and still above 25 µm. That margin also covers the dip of up to 5 µm that thermal.md found in a full-power heat-up, when the bore lags the plate.
2. **For Al powders the plate has to stay aluminium, and Al alloys barely change the answer.** Al printed on steel, Ti or Cu forms brittle Fe-Al, Ti-Al or Cu-Al intermetallics and bonds poorly. The piston alloy 4032 (12 % Si) closes ≥ 108 µm on L75 against 142 µm for 6061 (24 % less), so L75 would need ≥ 0.13 mm cold instead of 0.17; a printed, stress-relieved AlSi10Mg plate closes ≥ 118 µm. Both are lower bounds, because their datasheets give the CTE only to 100 °C: if 4032's rises by 200 °C as much as 6061's does (+0.8 µm/m·K), add ~5 µm on L75. Neither takes L75 back to 0.10 mm. The spray-formed hypereutectic Al-Si alloys (Osprey CE17, CE13) were not run: their datasheets are behind a login, so no checked numbers.
3. **Steel and titanium plates close 2–4 times less.** On L75: 430 49 µm, 17-4 PH 60 µm, Ti-6Al-4V 37 µm (316L 85 µm), against 142 µm for 6061. They suit the powders they match (steels and Ni alloys on 430 or 17-4 PH, Ti alloys on Ti-6Al-4V), and those are printed on matching plates anyway. The bore is fixed, so size each plate's diameter for its own material: L75 needs only 0.07 / 0.08 / 0.06 mm cold for 430 / 17-4 PH / Ti-6Al-4V. Cut to 6061's 0.20 mm they would run 140–163 µm hot, which widens the path for powder and heat. 410 behaves as 430 (48 µm on L75), and McMaster stocks it in thick sections, which it does not for 430.
4. **But low conductivity spreads the plate temperature.** With the centre held at 200 °C, the plate edge runs 7–8 °C cooler with 430, 10–11 °C cooler with 17-4 PH, 16–19 °C cooler with Ti-6Al-4V (6061: 1–2 °C), and the heater block runs hotter to push the heat through the plate. On S25 the block reaches 228 °C (430), 231 °C (17-4 PH), 231 °C (316L), 241 °C (Ti-6Al-4V), 239 °C (Invar 36), against 221 °C with 6061, the 240 °C cutoff and the ~225 °C block ceiling of the heat-up: S25 with a steel or Ti plate needs a higher cutoff and ceiling, or a thinner plate. Heater power stays within 3 W of 6061's.
5. **Invar 36 is a bound, not a candidate.** Its gap stays as cut (closing −3 to +2 µm), but McMaster stocks it only up to 1 in. rod, and its CTE climbs past its 279 °C Curie point, so it is no use for Tier B. The bore material is not a lever either (the bore option above).
6. **Tier B (500 °C) rules out aluminium plates.** 6061 closes ≥ 281 µm on M50 (≥ 0.31 mm cold needed; thermal.md's −61 µm used the 20–100 °C CTE) and 500 °C is 82 K under its solidus; 4032 is 30 K under its. In the 0.20 mm Tier B bore, Ti-6Al-4V leaves 109 µm, 430 87, 17-4 PH 65 and 316L 16. 430 sits in its 475 °C embrittlement range and 17-4 PH loses toughness above 316 °C (restored by re-ageing 4 h at 621 °C), so Ti-6Al-4V is the cleanest Tier B plate, then 17-4 PH. Expect 23–38 °C from centre to edge with these plates at 500 °C.

## Sources (read 2026-11-19)

1. [Kaiser Aluminum, Sheet Coil & Plate Alloy 6061, Rev. 05/06 (copy hosted by Protolabs)](https://Protolabs.com/media/1021492/6061-t651-cnc.pdf)
2. [ASM Aerospace Specification Metals / MatWeb, Aluminum 6061-T6 (Wayback copy: asm.matweb.com refused connections on 2026-11-19)](https://web.archive.org/web/20241217181844/https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA6061T6)
3. [Alcoa, Deltalloy 4032-T86 Aluminum (Knowde product page)](https://knowde.com/stores/alcoa-kama/products/deltalloy-4032-t86-aluminum)
4. [MakeItFrom, 4032-T6 aluminium (secondary database)](https://www.makeitfrom.com/material-properties/4032-4032-T6-AlSi12.5MgCuNi-Aluminum)
5. [3D Systems, LaserForm AlSi10Mg (A) datasheet, 2022-10-28](https://ko.3dsystems.com/sites/default/files/2022-10/3d-systems-laserform-alsi10mg%28a%29-datasheet-usen-2022-10-28-a-print.pdf)
6. [TIMET, TIMETAL 6-4 datasheet](https://www.timet.com/documents/datasheets/alpha-and-beta-alloys/timetal-6-4.pdf)
7. [Aubert & Duval, TA6V datasheet](https://www.aubertduval.com/wp-content/uploads/2024/12/TA6V_2_GB.pdf)
8. [Cleveland-Cliffs, 17-4 PH Stainless Steel product data bulletin, 05/2021](https://d1io3yog0oux5.cloudfront.net/_7ce3a04c09e74bf31ff5f89fc888db25/clevelandcliffs/db/1190/10503/file/CLF_ProductData_17-4-PHSS_052021.pdf)
9. [Austral Wright Metals, Stainless Steel Grade 430](https://www.australwright.com.au/technical-data/alloys/stainless-steel/stainless-steel-grade-430/)
10. [Cleveland-Cliffs, Ferritic Stainless Steel Automotive Trim (Type 430), 02/2025](https://www.clevelandcliffs.com/_assets/_799e54d4b8d0adcdcf958072b7e97a72/clevelandcliffs/db/1190/11606/file/CLF_ProductData_Ferritic+Automotive+Trim_022025.pdf)
11. [Atlas Steels, Stainless Steel 410 Grade Data Sheet, revised 28/04/2021](https://atlassteels.com.au/stainless-steel-410-grade-data-sheet-28-04-21)
12. [Cleveland-Cliffs, 316/316L Stainless Steel product data bulletin, 05/2021](https://d1io3yog0oux5.cloudfront.net/_464c1f648dd1e0c96c45d68cdce1cf31/clevelandcliffs/db/1190/10513/file/CLF_ProductData_316-316LSS_052021.pdf)
13. [High Temp Metals, Invar 36 technical data](https://hightempmetals.com/techdata/hitempInvar36data.php)

## Checks

- The 6061 rows reproduce thermal.json's build-start cases exactly (plate and bore-ring mean temperatures and heater power to 0.00 °C and 0.00 W). The closed form on thermal.json's temperatures gives the same closing: 50.6 / 97.6 / 141.9 µm by hand against 50.6 / 97.6 / 141.9 µm (S25 / M50 / L75).
- A hand estimate for every plate, with the plate uniformly at 200 °C and the bore at 6061's FEA temperature, is within 0.9 µm of the FEA closing: the plate's own ΔT and CTE set the answer, and the bore ring moves by ≤ 1.2 °C between plates.
- Mesh, energy balance and ccx conventions as in thermal.md (1 mm elements; 1D checks here: annulus +0.00 %, film +0.00 %, rad -0.15 %). Every case converged in 4–5 secant steps; energy balance ≤ 0.02 %.
- rho and c are written to the ccx deck but do not enter a steady solve; AlSi10Mg's c is 6061's, as a placeholder.
- Hot clearances are steady build start. The build end is looser (the bore warms to ~110 °C, thermal.md).
