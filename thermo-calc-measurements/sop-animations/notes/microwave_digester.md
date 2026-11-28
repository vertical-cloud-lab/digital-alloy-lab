# `microwave_digester`: CEM MARS 6 (SOP 05)

The model is `microwave_digester()` in [`models_chem.py`](../models_chem.py). It appears in chapter 4, where the
contract lab digests the samples before ICP-OES. It isn't registered to frames: it is a supporting instrument, built
from published figures with estimated proportions.

| | Published | Model | Source |
|---|---|---|---|
| W × D × H | 21 × 25 × 25 in = 533 × 635 × 635 mm, 140 lb (63.6 kg) | 533 × 635 × 635 (plus the door's handle and a 50 mm exhaust stub) | CEM MARS 6 Operation Manual rev. 8 (2011), specifications, p. 97 (CEM's PDF, hosted by NJIT) |
| Power, cavity | 1800 W at 2450 MHz; PFA-coated 316 stainless cavity | – | same; CEM brochure B098 p. 3 |
| Vessels | EasyPrep Plus: 12 × 100 mL, 300 °C, 800 psi; MARSXpress: 40; iPrep: 16 | 12 vessels on a turntable | CEM brochure B098 p. 6; manual p. 33 |

## Joints

`door` (a hinge at the left, 100°), `carousel` and `vessels` (one turn).

## Uncertain

- **Proportions.** The door's size and position, the cavity, the control panel and the turntable's radius (130 mm)
  are estimates from CEM's product photos.
- **The program shown** ("ramp to about 200 °C, hold about 15 min") is marked typical. Edison's source (Yamani 2021,
  doi:10.1016/j.arabjc.2021.103174) digests 150 mg of Al alloy in 3.0 mL HNO3 and 5.0 mL HCl. CEM's "Alum" note uses
  HCl, HF and HNO3 at 200 °C, then boric acid at 170 °C. That note covers alum rather than an Al alloy, so the program
  in the video is only typical. The lab's own method sets it.
