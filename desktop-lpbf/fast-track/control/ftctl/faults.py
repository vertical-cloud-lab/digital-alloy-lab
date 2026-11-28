"""Faults the supervisor detects, and what it does about each.

The hard-wired chain acts on its own and first (the G9SE-201 opens the laser's interlock, the CN708 opens K2, the
room O2 monitor's relay closes the argon valve). The supervisor sees the result on its inputs, stops the scan card
and the stages, records the fault and goes to SAFE_STOP. Nothing here is needed for the hardware to be safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Code(str, Enum):
    INTERLOCK_OPEN = "INTERLOCK_OPEN"
    LASER_FAULT = "LASER_FAULT"
    BACK_REFLECTION = "BACK_REFLECTION"
    SCANNER_FAULT = "SCANNER_FAULT"
    COOLING_FAULT = "COOLING_FAULT"
    RTC_ERROR = "RTC_ERROR"
    O2_HIGH = "O2_HIGH"
    O2_TIMEOUT = "O2_TIMEOUT"
    ROOM_O2_LOW = "ROOM_O2_LOW"
    STAGE_FAULT = "STAGE_FAULT"
    TC_OPEN = "TC_OPEN"
    PLATE_OVERTEMP = "PLATE_OVERTEMP"
    LIMIT_TRIPPED = "LIMIT_TRIPPED"
    HEAT_TIMEOUT = "HEAT_TIMEOUT"
    DWELL_TIMEOUT = "DWELL_TIMEOUT"
    WINDOW_HOT = "WINDOW_HOT"
    STRAY_BEAM = "STRAY_BEAM"
    BOX_AIR_HOT = "BOX_AIR_HOT"
    IO_LINK_LOST = "IO_LINK_LOST"
    OPERATOR_STOP = "OPERATOR_STOP"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# code -> (how it is detected, what the supervisor does, what acts without the supervisor)
TABLE = {
    Code.INTERLOCK_OPEN: ("G9SE-201 status output low (Pi input SAFETY_OK) or the laser's PS Active output drops while "
                          "the build runs",
                          "stop_execution, analog 0, EMOFF, stop both stages where they are (a person may be at the "
                          "lid), heaters stay under their controllers",
                          "G9SE outputs open the laser's two interlock channels: diode power off within 500 ms "
                          "(IPG guide)"),
    Code.LASER_FAULT: ("laser Error/Ready output low, or STA bits: overheat (1), module disconnected (6), power supply "
                       "off/failure (11, 19, 25), low temperature (24), critical error (29), optical interlock (30), "
                       "average power too high (31)",
                       "stop_execution, EMOFF, stop stages, log the STA word and RMEC code", "the laser's own protection"),
    Code.BACK_REFLECTION: ("STA bit 3 'High Back Reflection Level' (polled at 5 Hz during a scan) or the Error/Ready "
                           "output",
                           "as LASER_FAULT; the build is not resumed until the plate and the layer are inspected "
                           "(Edison round 2 ranks back reflection the top risk for the used laser)",
                           "the laser's back-reflection protection, if this unit has it (ask IPG with the serial)"),
    Code.SCANNER_FAULT: ("RTC5 get_head_status: Power or Temperature status not OK (XY2-100 status via the converter)",
                         "stop_execution, EMOFF, stop stages",
                         "set_laser_control bits 16, 17, 19, 20 + 28: the RTC5 suppresses the laser signals and stops "
                         "the list on its own"),
    Code.COOLING_FAULT: ("scan head water flow switch open (Pi input WATER_OK) while the laser is armed",
                         "stop_execution, EMOFF, SAFE_STOP: the entrance aperture is water-cooled", "-"),
    Code.RTC_ERROR: ("get_last_error != 0, or a list that runs past its planned time by > 1 s", "stop_execution, EMOFF",
                     "-"),
    Code.O2_HIGH: ("box O2 > o2_trip_ppm while a layer is being scanned", "stop_execution (the layer is aborted and "
                   "logged incomplete), EMOFF, keep argon flowing, SAFE_STOP", "-"),
    Code.O2_TIMEOUT: ("box O2 stays above o2_start_ppm for o2_hold_timeout_s before a layer, or the start-up purge "
                      "does not reach it within purge_timeout_s", "SAFE_STOP with argon flowing", "-"),
    Code.ROOM_O2_LOW: ("Macurco OX-6 relay (Pi input ROOM_O2_OK) or its 4-20 mA below 19.5 %",
                       "SAFE_STOP, argon valve request off, alarm; people leave the room",
                       "the OX-6 relay is in series with the argon valve coil and closes it"),
    Code.STAGE_FAULT: ("Zaber warning flags starting with F (FS stalled, FD driver disabled, FE limit error, FT twist, "
                       "FQ encoder, FM motor temperature, FV voltage, FF critical ...), a move that overruns its "
                       "planned time, or a position error > 0.05 mm after a move",
                       "stop both stages, stop_execution, EMOFF, SAFE_STOP", "-"),
    Code.TC_OPEN: ("a thermocouple reads open (PID controller sensor-break code, MCC 134 open-TC value) or NaN",
                   "heaters off (HEAT_EN relay drops K1), stop_execution, EMOFF, SAFE_STOP",
                   "the PID controller's sensor-break action turns its SSR off; the CN708 trips on its own open TC"),
    Code.PLATE_OVERTEMP: ("plate or block > soft_limit_C", "heaters off (K1), stop_execution, EMOFF, SAFE_STOP",
                          "CN708 trips at limit_C and opens K2 (latching, manual reset)"),
    Code.LIMIT_TRIPPED: ("CN708 status input low (its relay opened K2)", "heaters off (K1), SAFE_STOP",
                         "K2 is already open"),
    Code.HEAT_TIMEOUT: ("plate and block not within ready_band_K of the set point after heat_timeout_s",
                        "heaters off, SAFE_STOP", "-"),
    Code.DWELL_TIMEOUT: ("the plate stays above setpoint + dwell_band_K for dwell_max_s between layers",
                         "heaters off, SAFE_STOP", "-"),
    Code.WINDOW_HOT: ("window-ring thermocouple > window_fault_C (warning logged at window_warn_C): a fouled cover "
                      "slide absorbs the beam", "stop_execution, EMOFF, SAFE_STOP; replace the cover slide", "-"),
    Code.STRAY_BEAM: ("beam-tube thermocouple > beam_tube_fault_C", "stop_execution, EMOFF, SAFE_STOP",
                      "bimetal temperature switches on the beam tube and window ring open both G9SE input channels "
                      "at stray_switch_C"),
    Code.BOX_AIR_HOT: ("box air > box_air_fault_C (holds between layers above box_air_hold_C)",
                       "stop_execution, EMOFF, SAFE_STOP", "-"),
    Code.IO_LINK_LOST: ("no reply from the Pi I/O node for 2 s", "stop_execution, EMOFF, stop stages, SAFE_STOP",
                        "the Pi node's own watchdog drops HEAT_EN and the vibrator after 5 s without a request"),
    Code.OPERATOR_STOP: ("stop button in the UI or Ctrl-C", "graceful: finish the layer then SAFE_STOP; abort: as "
                         "INTERLOCK_OPEN", "-"),
    Code.INTERNAL_ERROR: ("an exception from a device driver or the supervisor itself", "as INTERLOCK_OPEN", "-"),
}


@dataclass
class Fault(Exception):
    code: Code
    message: str
    t: float = 0.0
    data: dict = field(default_factory=dict)

    def __str__(self):
        return f"{self.code.value}: {self.message}"
