# Bench templates

**`step-log.csv`**: one row per step per candidate or lot, filled at the bench. Table 1 and Fig. 1b of the article
are built from it. The optimizer's step costs come from it too.

| Column | What to write |
|---|---|
| `step` | one of: `calphad`, `charge`, `atomize`, `sieve`, `sem`, `eds`, `print`, `section`, `density`, `hardness`, `tensile`, `corrosion`, `outside` |
| `started`, `ended` | wall-clock times of the hands-on part |
| `people`, `person_hours` | how many people, and the sum of their hours |
| `machine`, `machine_hours` | instrument and how long it was occupied, including cleaning |
| `consumables`, `consumables_usd` | parts used up (plates, nozzles, crucibles, argon, powder) and their cost |
| `outside_fee_usd` | fees paid to another facility |
| `outcome` | `valid`, `failed` (step ran, result unusable) or `abandoned` (stopped on purpose); see #274 |

The atomizer's own run record stays the YAML template in byu-vcl `atomizer-runs/plan-adv-mater/run-record-template.yaml`.
This log covers every step, not just atomization.
