# The aging station's props (models_props.py)

## `aging_rack`: tray, five boats, 20 coupons (our layout)

| Part | Size | Why |
|---|---|---|
| Tray | 160 × 120 × 14 mm, 1.2 mm stainless; drain slots; a 12 mm tab at the front for the tongs | It fits the NAT 15/65's chamber (300 × 340 × 150 mm in byu-vcl's model, 15 L) with room for the tongs. |
| Boats | 5 × (26 × 110 × 5 mm), 0.8 mm sheet; a 10 mm tab forward over the tray's rim | One boat per aging time (0.25, 1, 4, 16, 64 h), so each time point is one pick with the tongs and one door opening. |
| Coupons | 10 × 10 × 3 mm, four per boat: candidate, AlSi10Mg, 6063, Scalmalloy-type | SOP 04 Samples: flat coupons ≥ 10 × 10 mm and ≥ 2 mm; the references go through the same matrix. |

Edison (v3, `edison/v3-hardness-eddy-icp-onh/answer.md` §3) gives the practice the animation follows:

- **Preheat the empty furnace to set point.**
- **Coupons:** a single layer of marked coupons on a low-mass stainless tray, with gaps for air.
- **Insert the tray quickly**, and start the soak only when a check thermocouple beside the coupons is back at
  set point.
- **Take coupons out with tongs** at their times.

The thermocouple is drawn as a fine type K wire through the door seal on the hinge side. Its bead lies on the
chamber floor beside the tray, and its reader sits on the bench.

Edison also notes that published direct aging of Scalmalloy usually cools in air. Water quenching is
documented for solution-treated AlSi10Mg. SOP 04 specifies a water quench at every time point, which freezes
the state for the kinetics, so the animation follows the SOP. This is flagged in `notes/sop04.md`.

## `tongs`

Crucible / furnace tongs, about 400 mm (16 in), scissor-type, plated steel; proportions estimated.

- **The jaws** are bent up 20°, so they are level when the tongs are held 20° down. The trays and boats then hang
  level from their tabs.
- **The upper jaw** opens on the pivot (`arm_a`, a hinge). The lower jaw stays level under the tab.

## `quench_bath`

A stainless bath the size of byu-vcl's quench tank (240 × 200 × 210 mm, `r8_test.QUENCH`), filled with tap water
to 165 mm. It has a lift-out mesh basket with a bail handle.

byu-vcl's tank was not reused, for two reasons:

- its basket rides a pneumatic cylinder behind the tank, built for the robot arm;
- its arm passes through the tank's back wall as it moves.

## `lab_timer`, `tc_reader`, `thermometer`

| Prop | Size | Display |
|---|---|---|
| `lab_timer` | 70 × 20 × 75 mm | LCD |
| `tc_reader` (handheld type K reader) | 75 × 32 × 150 mm | LCD |
| `thermometer` (room thermometer / hygrometer) | 100 × 22 × 100 mm | LCD |

All three are common sizes, estimated.

## `furnace_hinged`: byu-vcl's NAT 15/65 with real hinges

byu-vcl's Nabertherm NAT 15/65 (`instruments.furnace`, fitted to Nabertherm's video) drew its two hinges as solid
blocks across the door's swing, so the door passed through them as it opened. The audit flagged this (60 mm).

Here each block is a knuckle round the door's pivot, with one leaf on the cabinet's side and one on the door's
front. The chamber floor's front edge is also 3 mm shorter, clear of the door plug. Nothing else changes, so
byu-vcl's fit (1.2 and 6.3 px on Nabertherm's video) still applies.

## `hv_manual`: byu-vcl's HM-220, for a person

byu-vcl's Mitutoyo HM-220 is in `instruments_r7.hardness` (Mitutoyo catalogue section K: 315 × 671 × 595 mm,
43 kg). It keeps that model's base, column, head, camera, turret and objectives and its AVPAK PC.

| byu-vcl's round-8 version | `hv_manual` |
|---|---|
| A robot loading slide and V-block holder | Left out |
| — | The elevating screw lowers the stage 60 mm on the left handwheel, to set a 38 mm mount by hand |
| XY table | Steps in mm |
| Turret | Turns in degrees: 0 the 50x objective, +90 the 10x, −90 the indenter |
| Indenter | Comes down 3 mm onto the face |
| Diamond | A 136° square pyramid |

Added: a monitor on the PC (an estimate, like byu-vcl's PC and joystick).
