"""Machine parameters for FT-1, each with its source. "estimate" means nobody has measured or read it yet.

Units: mm, s, W, degrees C, L/min, ppm (O2 by volume). Frame: cad/ft_model.py (origin at the centre of the substrate's
top face at the start of a build, +X recoat direction, +Y to the back).
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field


@dataclass
class Gas:
    box_volume_L: float = 23.5          # FT-1 gas volume measured in the CAD model (cad/README.md)
    purge_flow_Lpm: float = 20.0        # study 3.4: purge at 20 L/min
    build_flow_Lpm: float = 27.0        # study 3.4: 45 x 4 mm slot nozzle at 2.5 m/s, ~27 L/min once-through
    idle_flow_Lpm: float = 5.0          # keeps the box at +5-10 mbar while cooling (estimate)
    mixing_factor: float = 3.0          # study 3.4: real purge takes 2-5x the perfect-mixing time; mid value (estimate)
    argon_o2_ppm: float = 2.0           # UHP argon, O2 <= 1-2 ppm (supplier class spec; estimate)
    floor_ppm: float = 150.0            # leak + permeation floor at the purge flow (estimate; the analyzer measures it)
    air_o2_ppm: float = 209_460.0       # dry air
    o2_start_ppm: float = 1000.0        # a layer starts only below this (EOS M 290 Al threshold, study 3.4)
    o2_trip_ppm: float = 1500.0         # a running layer is aborted above this (estimate: start threshold x 1.5)
    o2_hold_timeout_s: float = 600.0    # wait this long for O2 to come back under o2_start_ppm before a fault (estimate)
    purge_timeout_s: float = 3600.0     # start-up purge must reach o2_start_ppm within this (study: 13-31 min expected)
    heat_below_ppm: float = 10_000.0    # heaters may start once O2 < 1 % while the purge goes on (estimate)
    analyzer_t90_s: float = 30.0        # electrochemical trace cell, 90 % response (estimate; not in the Series 3000 sheet)
    analyzer_range_ppm: float = 10_000.0  # Alpha Omega Series 3000: ranges 0-1 ppm up to 0-10,000 ppm (datasheet)
    trace_open_below_pct: float = 1.5   # open the trace cell's sample valve only below this (keeps the cell out of air)
    pct_t90_s: float = 15.0             # percent-range O2 transmitter on the exhaust, 0-25 % (estimate)
    vent_flow_Lpm: float = 10.0         # slow air vent through the inlet filter after a build (estimate)
    open_o2_ppm: float = 195_000.0      # lid may open at >= 19.5 % O2 (NIST AMMT practice, study 3.7)
    room_alarm_pct: float = 19.5        # Macurco OX-6 low alarm (OSHA oxygen-deficient atmosphere)


@dataclass
class Thermal:
    setpoint_C: float = 200.0           # plate and well block (study 3.3)
    ambient_C: float = 35.0             # box air with the fan on the box: 9-14 K rise (study 3.5)
    # Heat capacities from the CAD sizes (cad/README.md) with 6061 at 2.70 g/cm3 and 0.896 J/(g K):
    plate_JK: float = 105.0             # plate O39.8 x 28 mm (94 g) + substrate O39.8 x 6 mm (20 g) + heaters
    block_JK: float = 460.0             # 80 x 80 x 40 mm block less the O40 bore and 7 x 44 mm slot (~513 g)
    plate_heater_W: float = 100.0       # 2 x 50 W, 24 V (McMaster 3714N36)
    block_heater_W: float = 100.0       # 2 x 50 W, 24 V
    # Loss conductances: the study's ~56 W load at 200 C (study 3.5) split by surface (estimate):
    plate_loss_WK: float = 0.03         # top face radiation + convection in argon + the rod's ~2 W (cad/README.md)
    block_loss_WK: float = 0.30
    plate_block_WK: float = 0.9         # argon (k ~0.025 W/m K at 200 C) across the 0.1 mm radial gap, 3,510 mm2
    tc_tau_s: float = 2.0               # sheathed type K in a drilled hole (estimate)
    absorptivity: float = 0.45          # of the laser energy into the plate; study 3.5 uses 0.3-0.6
    ready_band_K: float = 3.0           # heat-up is done when plate and block are within this ...
    ready_hold_s: float = 60.0          # ... for this long
    heat_timeout_s: float = 2700.0      # 45 min (estimate; the model reaches 200 C in ~15-20 min)
    dwell_band_K: float = 5.0           # next layer starts only when the plate is <= setpoint + this (PR 266 used +3 K)
    dwell_max_s: float = 600.0          # a dwell longer than this is a fault (heater stuck on, or a TC drifted)
    block_offset_K: float = 0.0         # block set point = plate set point + this during the build (study option:
                                        # -20 K moves the plate-block gap by 23.6e-6/K x 20 K x 40 mm / 2 = 9 um radial)
    soft_limit_C: float = 225.0         # supervisor's plate/block over-temperature fault (estimate)
    limit_C: float = 240.0              # CN708 latching limit on its own thermocouple, opens K2 (estimate)
    box_air_hold_C: float = 45.0        # hold between layers above this: Zaber stages are rated 0-50 C
    box_air_resume_C: float = 42.0
    box_air_fault_C: float = 50.0
    window_warn_C: float = 55.0         # window ring: cover-slide fouling shows here first (Edison round 2; estimate)
    window_fault_C: float = 65.0         # below stray_switch_C, so software stops first and the switch is the backstop
    beam_tube_fault_C: float = 60.0     # stray-beam sensor (study 3.7; estimate)
    stray_switch_C: float = 75.0        # bimetal temperature switches in the safety chain (estimate)
    open_plate_C: float = 60.0          # vent only below this, so hot fresh condensate meets air slowly (estimate)
    pid_plate: tuple = (0.06, 150.0)    # (Kp per K, Ti s) for the simulated controllers; the real ones autotune
    pid_block: tuple = (0.10, 400.0)


@dataclass
class Motion:
    layer_mm: float = 0.030             # process/scan_program.py CUBE_SET
    # Piston: Zaber X-VSR20A-E01, 20 mm, 48 mm/s, 100 N (zaber.com, read 2026-11-27)
    piston_travel_mm: float = 20.0
    piston_build_start_mm: float = 15.5  # plate top level with the well top (estimate: set at commissioning)
    piston_min_mm: float = 0.3
    piston_step_speed: float = 5.0      # process/scan_program.py
    piston_accel: float = 200.0         # estimate (Zaber default class)
    # Recoater: Zaber X-LSM100B-E03, 101.6 mm, 104 mm/s, 25 N (zaber.com, read 2026-11-27)
    recoater_travel_mm: float = 101.6
    recoater_offset_mm: float = 48.5    # stage position = machine X + this (estimate, puts the parks mid-travel)
    park_left_x: float = -30.9          # hopper parks clear of the beam (cad/README.md, drawn for the X-LSQ075B)
    park_right_x: float = 35.5
    spread_speed: float = 40.0          # forward stroke that lays the layer (process/scan_program.py; estimate)
    return_speed: float = 104.0         # the X-LSM100B's maximum
    recoater_accel: float = 1000.0      # estimate
    settle_s: float = 0.10              # after the plate step (process/scan_program.py)
    move_timeout_margin_s: float = 5.0  # a move that takes this much longer than planned is a fault

    def stage_x(self, x_machine: float) -> float:
        return x_machine + self.recoater_offset_mm


@dataclass
class Laser:
    model: str = "IPG YLR-400-SM-EOS (Feb 2015)"
    p_max_W: float = 400.0
    analog_min_V: float = 1.0           # IPG YLR-series user guide, 24-pin table: 1-10 V = 10-100 % setpoint
    analog_max_V: float = 10.0
    min_setpoint_pct: float = 10.0
    # Setpoint % -> output W, measured with the calorimetric check on arrival; linear until then (estimate)
    calibration: tuple = ((10.0, 40.0), (100.0, 400.0))
    serial_port: str = "COM3"
    baud: int = 57600                   # 24-pin generation guide; a 2015 EOS unit may differ (measure)
    first_test_W: float = 50.0          # first powered tests ~50 W on an anodised plate off the field centre (Edison r2)

    def setpoint_pct(self, P: float) -> float:
        """Laser setpoint (% of maximum current) for P watts, interpolated in the calibration table and clamped to
        [min_setpoint_pct, 100]. P <= 0 returns 0 (the gate is off anyway)."""
        if P <= 0:
            return 0.0
        pts = sorted(self.calibration, key=lambda t: t[1])
        s = pts[-1][0]
        for (sa, pa), (sb, pb) in zip(pts, pts[1:]):
            if P <= pb:
                s = sa + (sb - sa) * (P - pa) / (pb - pa)
                break
        return min(max(s, self.min_setpoint_pct), 100.0)

    def analog_V(self, P: float) -> float:
        """Voltage on the laser's analog input for P watts (1-10 V = 10-100 %, IPG YLR-series user guide)."""
        s = self.setpoint_pct(P)
        return 0.0 if s <= 0 else self.analog_max_V * s / 100.0


@dataclass
class Scan:
    # RTC5 (manual Rev. 1.9 e): 10 us list clock; coordinates 20-bit signed in the real field; K = 2^20 / a0 bits/mm
    field_angle_rad: float = 0.35       # hurrySCAN 20/25/30 typical scan angle (optical), SCANLAB brochure
    focal_mm: float = 254.0             # LINOS F-Theta-Ronar 4401-288-000-20 (EFL 254.4 mm)
    K_bits_per_mm: float = 0.0          # 0 = 2^20 / (2 f theta); the real K comes from get_table_para(1, 1)
    x_offset_mm: float = 0.0            # lens axis to machine origin (process/optics.py; set with the burned grid)
    y_offset_mm: float = 0.0
    swap_xy: bool = False               # head mounting: set at commissioning from the burned grid
    flip_x: bool = False
    flip_y: bool = False
    rtc_dir: str = r"C:\RTC5"           # RTC5OUT.out, RTC5RBF.rbf, RTC5DAT.dat (SCANLAB download portal)
    correction_file: str = r"C:\RTC5\ft1_hs25_f254.ct5"  # made with correXion from a burned grid (not yet made)
    xy2_converter_latency_s: float = 10e-6  # SCANLAB XY2-100 converter, add to both laser delays (manual p. 42)
    record_trace: bool = True           # set_trigger4: LASERON, SampleX, SampleY, ANALOG OUT1 at 10 us per layer

    def K(self) -> float:
        if self.K_bits_per_mm > 0:
            return self.K_bits_per_mm
        return 2 ** 20 / (2.0 * self.focal_mm * self.field_angle_rad)


@dataclass
class Config:
    gas: Gas = field(default_factory=Gas)
    thermal: Thermal = field(default_factory=Thermal)
    motion: Motion = field(default_factory=Motion)
    laser: Laser = field(default_factory=Laser)
    scan: Scan = field(default_factory=Scan)
    poll_s: float = 0.05                # supervisor's poll period while waiting (real time)
    sample_s: float = 1.0               # log period of the slow channels
    overlap_heat_with_purge: bool = True
    argon_low_in_dwell: bool = True     # cross-flow only while recoating and scanning; the low flow holds the box in dwells
    flow_settle_s: float = 2.0          # main flow back on this long before a scan that follows a dwell (estimate)
    camera: bool = True
    vent_after_build: bool = True

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=1, default=str)


def perfect_mixing_minutes(gas: Gas, target_ppm: float, flow_Lpm: float | None = None) -> float:
    """Ideal flow-purge time from air to target (the study's table): ln(C0/C) volume changes."""
    q = flow_Lpm or gas.purge_flow_Lpm
    return math.log(gas.air_o2_ppm / target_ppm) * gas.box_volume_L / q
