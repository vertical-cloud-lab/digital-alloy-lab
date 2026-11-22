# IPG YLR-500-U3-SM-AC: budgetary quote and spec sheet (2026-11-18)

Sterling asked IPG for a budgetary quote on a 500 W single-mode CW fiber laser for this machine (BOM line L1). IPG's scientific laser sales manager replied on 2026-11-18.

## Quote

| | |
|---|---|
| Model | **YLR-500-U3-SM-AC**, IPG's current 500 W single-mode unit (offered in place of the YLR-500-WC-Y14 we named) |
| Price | **approximately $23k** (rounded to the nearest $1k) |
| Lead time | **10–12 weeks ARO** (after receipt of order) |
| Expediting | Sterling asked; IPG said it is "unlikely to deliver much faster than 10-12 weeks" |

**The lead time puts the laser on the critical path.** Ten to twelve weeks starts when IPG receives the PO, not when we decide. Above $3,500 BYU needs a purchase order, which adds its own processing time. So an order placed in early December lands around late February to mid-March 2027, and a later order slips the CW phases ([README](../README.md) §5, phases 2–3) week for week. If the CW component route is the likely outcome of the go/no-go point, the laser order has to go in before that point, not after it.

IPG asked us to confirm the spec sheet works before sending the rest. **Still to come from IPG:** warranty, academic pricing, country of manufacture, a STEP model, the collimator price, a 300 W price, back-reflection protection, the interlock and modulation interface details (the spec sheet points to the YLR-U3 Series User Guide), and whether they offer a safety shutter.

## Specifications (IPG spec G22-29856 rev. 00, dated 03.02.2025)

Transcribed from the spec sheet IPG attached. The PDF itself isn't committed.

### Optical

| Characteristic | Conditions | Min | Typ | Max | Unit |
|---|---|---|---|---|---|
| Operation mode | | | CW / modulated | | |
| Polarization | | | random | | |
| Nominal output power | | 500 | | | W |
| Emission wavelength | 500 W | | 1070 | | nm |
| Emission linewidth | 500 W | | 4 | 5 | nm |
| Short-term power instability | 500 W, 10 kHz–20 MHz | | 1.0 | 2.0 | % rms |
| Long-term power instability | 500 W, 4 h, constant T | | ±1 | ±3 | % |
| Switching on/off time | 500 W | | | 12 | µs |
| Power modulation rate | 500 W | | | 100 | kHz |
| Red guide laser power | | 0.1 | | 1.0 | mW |

### Optical output

| Characteristic | Min | Typ | Max | Unit |
|---|---|---|---|---|
| Beam quality M² | | 1.05 | 1.1 | |
| Delivery fiber length | | 5.0 | TBD | m |
| Delivery cable bending radius | 70 | | | mm |
| Output termination | QBH-compatible connector (default) or collimator | | | |
| Beam divergence, bare QBH output (full angle, 86 %, fiber ≤ 10 m) | 130 | 140 | 150 | mrad |

- **Standard collimators:** 5 mm or 7.5 mm beam diameter; other diameters on request.
- **Attachable collimators:** D25F50, D25F60, D25F85, D50F100, D50F120, D50F160, D50F200.
- **Other accessories:** compact beam coupler BC1x112; compact beam switch BS1xN12 (1–4 output channels).

### General and electrical

| Characteristic | Value |
|---|---|
| Cooling | **forced air** (no chiller) |
| Operating ambient | 10–35 °C, 10–95 % humidity |
| Storage | −20 to +60 °C |
| Package | 4U 19 in. rack mount, 448 × 506 × 177 mm (W × D × H) |
| Weight | 40 kg |
| Supply | 200–240 VAC single-phase, 50/60 Hz |
| Max power draw | 1,500 W typ / 1,700 W max; 1,600 VA typ / 1,900 VA max |
| Control | analog / RS-232 / Ethernet (details in the YLR-U3 Series User Guide) |
| Laser class | Class 4 (1 kW CW max, 900–1,200 nm label); guide laser Class 2M |

### Mechanical (from the drawings)

- **Cabinet:** 482.3 mm wide over the rack ears (465 mm body), 557.2 mm deep over the handles (506 mm body), 176.5 mm tall; fans on the front panel.
- **QBH-compatible connector:** about 190.6 mm long overall, Ø20 mm body, Ø8.5 mm cable.
- **Collimator, 5 mm beam:** Ø30 mm housing (Ø28 mm at the output end), 128 ± 3 mm long, plus 78 mm of strain relief behind it.
- **Collimator, 7.5 mm beam:** the same diameters, 143 ± 3 mm long.

## Against the request and README §3.2

| We asked for | Spec sheet |
|---|---|
| 1070 nm, M² ≤ 1.1 | ✅ 1070 nm, M² 1.05 typ / 1.1 max |
| CW with fast modulation (µs gate) | ✅ CW/modulated, ≤ 12 µs on/off, to 100 kHz (README §3.2 had 0–50 kHz for the older YLR) |
| Analog power control, gate input, interlock input, guide laser | ✅ analog control and a 0.1–1 mW red guide laser. ❓ Gate and interlock inputs aren't listed; they are in the U3 user guide |
| Back-reflection protection for Al | ❓ not on the spec sheet: ask IPG to confirm in writing |
| ~5 m fiber and a collimator for a 20 mm galvo (3–5 mm beam) | ✅ 5 m fiber; 5 mm standard collimator. Price not yet given |
| Air cooling if available | ✅ forced air, so BOM line L2 drops to $0 for this laser |
| 200–240 VAC single-phase | ✅, at up to 1.9 kVA: plan a dedicated circuit |
| Optional safety shutter | ❓ not listed; BOM line L4 stays |

**What it changes in the design:**
- No chiller and no coolant loop next to the machine. The cabinet needs front-panel airflow and an ambient of 35 °C or less.
- The 4U, 40 kg rack box sits beside the cabinet, as the layout already assumes. The 70 mm minimum bend radius sets the fiber routing into the optics bridge.
- With D = 5 mm and f = 254 mm, the spot is about 76 µm (README §3.2), so no beam expander is needed. The 7.5 mm collimator would give about 51 µm.
