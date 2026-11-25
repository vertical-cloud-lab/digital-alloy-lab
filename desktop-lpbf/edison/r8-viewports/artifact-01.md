| Material | Modulus of rupture, psi / MPa | Poisson’s ratio | Thermal conductivity, W·m⁻¹·K⁻¹ | Maximum service temperature, °C | Robinson coefficient, `k`, in `t = d k √(q·F/S)` | Minimum thickness: 20 mm aperture, 1 bar, `F/S = 10` |
|---|---:|---:|---:|---:|---:|---:|
| Fused silica (quartz) | 7,000 / 48 | 0.16 | 1.38 | 1,000 | 0.0065 | **1.56 mm**: `t = 0.787 × 0.0065 × √(14.5×10) = 0.0616 in = 1.56 mm` (pqac-00000017, pqac-00000020, pqac-00000025) |
| Sapphire | 40,000 / 276 | 0.16 | 20.5 | 1,000 | 0.0027 | **0.65 mm**: `t = 0.787 × 0.0027 × √(14.5×10) = 0.0256 in = 0.65 mm` (pqac-00000017, pqac-00000022, pqac-00000005) |
| BK7 / annealed borosilicate¹ | 3,000 / 20.7 | 0.20 | ≈1.1 | ≈232 | 0.010² | **2.41 mm**: `t = 0.787 × 0.010 × √(14.5×10) = 0.0948 in = 2.41 mm` (pqac-00000017, pqac-00000022) |
| Tempered borosilicate¹ | 9,000 / 62.1 | ≈0.20 | ≈1.1 | ≈288 | ≈0.0058² | **≈1.39 mm**: coefficient scaled from annealed strength, `0.010√(3000/9000)` (pqac-00000017, pqac-00000022) |
| Tempered plate glass | 15,000 / 103 | 0.20 | ≈1.0 | ≈232 | 0.0045 | **1.08 mm**: `t = 0.787 × 0.0045 × √(14.5×10) = 0.0426 in = 1.08 mm` (pqac-00000017, pqac-00000020, pqac-00000022) |
| Design note | — | — | — | — | — | Values are plate-theory screening estimates for a simply supported, flawless circular window—not certified dimensions. Use minimum actual thickness, verify edge/contact and thermal stresses by FEA, and select a thicker standard plate; Robinson recommends a safety factor of 10 for brittle chamber windows (pqac-00000018, pqac-00000020, pqac-00000023) |
| ¹ Material caveat | — | — | — | — | — | BK7 and borosilicate/Pyrex are not interchangeable compositions; the tabulated strength and temperature values are for borosilicate glass. Obtain certified lot data before sizing a BK7 window. |
| ² Coefficient caveat | — | — | — | — | — | Robinson’s published `k = 0.010` is for annealed plate glass. It is used here as a conservative proxy for annealed borosilicate; the tempered-borosilicate value is derived by inverse square-root scaling with rupture strength and is not a published Robinson coefficient. |


*Table: Material properties and first-pass minimum thicknesses for a 20 mm circular viewport under a 1 bar differential. The calculations use Robinson’s simply supported brittle-plate equation and should be followed by certified-material and thermal-stress verification.*
