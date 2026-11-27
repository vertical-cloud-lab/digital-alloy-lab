# Atomizer runs: one row per logged run

[`runs.csv`](runs.csv) lists every logged run of the AMAZEMET rePOWDER ultrasonic atomizer from Oct 2 to Nov 13, 2026: ten runs, five of aluminum alloys and five of 630 nickel-aluminum bronze (C63000). AMAZEMET's training runs on Sep 29 and 30 are not included. Each row restates the run's log as reported, with links to it. Nothing here is new analysis.

| Date | Alloy, charge | Lot or sample code | Record |
|---|---|---|---|
| Oct 2 | Al 4047 powder in an Al 6063 cup (mass not recorded) | u23y78 | [Oct 8 record, "compared with earlier runs"](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/308f3c2/atomizer-runs/2026-10-08/README.md#compared-with-earlier-runs) |
| Oct 6 | Al 6063 (logged as "6067"), 180 g | 4yghtr | [issue 159 log](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159#issuecomment-6353392712) |
| Oct 8 | Al, three rods (not weighed) | kj0461 | [Oct 8 record](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/308f3c2/atomizer-runs/2026-10-08/README.md) |
| Oct 21 | Al 4047, 169 g | k7m2qx | [Oct 21 record](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/5d1cf0c/atomizer-runs/2026-10-21/README.md) |
| Oct 22 | Al 4047, 169 g | c3k0n5 | [issue 159 log](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159#issuecomment-6353395276) |
| Oct 27 | 630 bronze, 1,079.9 g | k7m2q9 | [issue 219 log](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6457884447), [sieve weights](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6509252104), [provenance](2026-10-27-nab-k7m2q9/provenance.md) |
| Oct 28 | 630 bronze, 858.4 g | (none logged) | [Oct 28 record](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/413e717/atomizer-runs/2026-10-28/README.md) |
| Nov 5 | 630 bronze, 952.5 g | n05oun (SEM sample) | [issue 219 log](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6670680314), [placeholder record](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/41d8ef7/atomizer-runs/2026-11-05/README.md) |
| Nov 10 | 630 bronze, 816.3 g | 834try (SEM sample) | [issue 219 log](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6782720747), [placeholder record](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/41d8ef7/atomizer-runs/2026-11-10/README.md) |
| Nov 13 | 630 bronze, 816.0 g | (none logged) | [Nov 13 record](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/1ea7c0e/atomizer-runs/2026-11-13/README.md) |

## Columns

| Column | Meaning |
|---|---|
| `date` | Run date (YYYY-MM-DD) |
| `alloy` | Charge alloy as logged |
| `charge_g` | Charge mass in grams; blank where it was not weighed or not recorded |
| `lot_or_sample_code` | Powder lot or SEM sample code, where one was assigned |
| `plate` | Atomizing plate (sonotrode tip): material, coating, and whether it was new or reused |
| `booster` | Ultrasonic booster ratio (reducing or amplifying) |
| `amplitude_pct` | Vibration amplitude setting, % |
| `melt_C` | Melt temperature, °C |
| `hold_min` | Hold at melt temperature before the pour, minutes |
| `graining_bar` | Pour (graining) pressure setting, bar; the turbo setting and display readings in parentheses where logged |
| `o2_ppm` | Chamber oxygen, ppm, as logged |
| `powder_result` | How much powder the run made, as logged |
| `result_basis` | Whether `powder_result` was weighed, estimated by the operator, or noted only |
| `outcome` | What happened, as logged |
| `changed_for_next_run` | What the log says changed, or was planned, for the next run |
| `sources` | Links to the log comments and run records, separated by ` ; ` |

## Notes

- **Only Oct 27 and Oct 28 were sieved and weighed**, together, as one lot (1,938.3 g charged). Oct 27's "about 91% below 250 µm" splits that pooled weight by estimate. The Oct 28 and Nov 10 figures are the operator's estimates, and no aluminum powder weights are recorded.
- **The Nov 5, Nov 10, Oct 21 and Oct 22 rows are as the logs report them.** Their analysis is left to the students in vertical-cloud-lab/digital-alloy-lab#252, so this table doesn't answer the questions there.
- **New runs add a row each**, including the campaign runs planned in vertical-cloud-lab/digital-alloy-lab#256.
