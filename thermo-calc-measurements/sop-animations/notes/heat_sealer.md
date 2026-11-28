# `heat_sealer`: an 8 in hand impulse sealer (Uline H-163 class) (SOP 05)

The model is `heat_sealer()` in [`models_chem.py`](../models_chem.py). It seals the poly bag of argon-flushed powder
for O/N/H in chapter 2. It isn't registered to frames: it is a small supporting tool, built from the published size.

| | Published | Model | Source |
|---|---|---|---|
| Overall | 3.2 D × 12.6 W × 5.9 H in = 81 × 320 × 150 mm, 6.45 lb, 410 W | 320 × 81 × 150 | [uline.com/Product/Detail/H-163](https://www.uline.com/Product/Detail/H-163) |
| Seal | 8 in × 1/16 in (203 × 1.6 mm) | a 203 mm jaw | same |

The jaw's height (101 mm), the arm and the timer's position are estimates from Uline's photos. The arm is the only
joint: `arm`, a hinge at the back, 35°. It starts open (v 1) and closes at v 0.
