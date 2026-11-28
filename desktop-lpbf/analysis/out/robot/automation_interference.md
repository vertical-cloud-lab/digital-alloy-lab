# Interference check of the robot-tending features (M50)

`analysis/robot/automation_check.py`, 640.6 s: interference.py's mesh + exact booleans for every pair that involves one of the 11 automation parts, in five states and through the sweeps of door, drawer, gdoor, recoater.

| State or sweep | Interferences |
|---|---|
| closed, parked, piston up | 0  |
| plate exchange: doors open, plate up 8 mm | 0  |
| doors open, reservoir and drawer out | 0  |
| recoater at the end, piston at the bottom stop | 0  |
| module swap: arm released, module dropped | 0  |
| sweep door | 0  |
| sweep drawer | 0  |
| sweep gdoor | 0  |
| sweep recoater | 0  |

Tightest gaps of the moving automation parts:

| Group | At | Moving | Other | Gap (mm) |
|---|---|---|---|---|
| door | 0.0 | Door drive shaft and disc (Ø6 D-shaft keyed into a 6061 disc | Door drive: pneumatic rotary actuator on the hinge axis, SMC | 0.0 |
| door | 7.92 | Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal | Drawer latch wing head, left (26 mm wing on the quarter-turn | 10.308 |
| door | 7.92 | Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal | Drawer latch wing head, right (26 mm wing on the quarter-tur | 10.308 |
| door | 43.54 | Draw latches on the door's latch brackets, pointing forward  | Door drive: pneumatic rotary actuator on the hinge axis, SMC | 10.552 |
| door | 0.0 | Door drive shaft and disc (Ø6 D-shaft keyed into a 6061 disc | Door hinge knuckles on the chamber (304 SS) | 12.1 |
| door | 0.0 | Door drive shaft and disc (Ø6 D-shaft keyed into a 6061 disc | Hinge pins (Ø5, 316) | 12.1 |
| door | 87.08 | Door drive shaft and disc (Ø6 D-shaft keyed into a 6061 disc | Chamber floor plate (6061-T6, 20 mm, bolted under the frame; | 13.0 |
| door | 0.0 | Draw-latch actuators: 2 x Ø20 compact air cylinders (SMC CJ2 | Optics bridge posts (60 x 60 x 5 square 6061 tube, 10 mm end | 14.0 |
| drawer | 0.0 | Drawer latch wing head, right (26 mm wing on the quarter-tur | Drawer-closed sensor (inductive M12, on the lid's front face | 2.0 |
| drawer | 0.0 | Drawer latch wing head, left (26 mm wing on the quarter-turn | Chamber lid (6061-T6, 16 mm, cover-slide drawer slot) | 11.5 |
| drawer | 0.0 | Drawer latch wing head, left (26 mm wing on the quarter-turn | Drawer latch receptacles in the lid (2 x quarter-turn latch) | 11.5 |
| drawer | 0.0 | Drawer latch wing head, right (26 mm wing on the quarter-tur | Chamber lid (6061-T6, 16 mm, cover-slide drawer slot) | 11.5 |
| drawer | 0.0 | Drawer latch wing head, right (26 mm wing on the quarter-tur | Drawer latch receptacles in the lid (2 x quarter-turn latch) | 11.5 |
| drawer | 0.0 | Drawer latch wing head, left (26 mm wing on the quarter-turn | Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal | 12.0 |
| drawer | 0.0 | Drawer latch wing head, right (26 mm wing on the quarter-tur | Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal | 12.0 |
| drawer | 0.0 | Drawer latch wing head, left (26 mm wing on the quarter-turn | Process chamber body (6061-T6 through-frame from 5.5 in. pla | 12.971 |
| gdoor | 493.54 | Guard-door handle for the robot (Ø12 x 130 bar on two Ø10 st | Laser guard panels (1.5 mm aluminium) | 6.0 |
| gdoor | 493.54 | Guard-door handle for the robot (Ø12 x 130 bar on two Ø10 st | Guard-position switch IDEC HS6B-12B05 (2NC + 1NO, tongue act | 11.006 |
| gdoor | 515.0 | Guard-door handle for the robot (Ø12 x 130 bar on two Ø10 st | Guard frame (20 mm T-slot) | 82.344 |
| gdoor | 0.0 | Guard-door handle for the robot (Ø12 x 130 bar on two Ø10 st | Guard door rail (top + bottom) | 191.158 |
| recoater | 8.58 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Dose chute (316L) | 4.243 |
| recoater | 0.0 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Process chamber body (6061-T6 through-frame from 5.5 in. pla | 22.091 |
| recoater | 85.83 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Floor-plate screws, M4 x 16 316, up through U-notches in the | 35.114 |
| recoater | 0.0 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Draw-latch strikes on the chamber's side faces (1807A61 stri | 48.374 |
| recoater | 0.0 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Floor-plate dowels, Ø6 x 20 316 (pressed into the plate, sli | 49.09 |
| recoater | 206.0 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Optics bridge posts (60 x 60 x 5 square 6061 tube, 10 mm end | 93.744 |
| recoater | 17.17 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Gas-loop + vacuum hoses (KF-25 SS bellows) | 100.661 |
| recoater | 206.0 | Blade-cartridge grip fin (6061, 4 mm, on the holder's front  | Laser guard panels (1.5 mm aluminium) | 207.239 |
