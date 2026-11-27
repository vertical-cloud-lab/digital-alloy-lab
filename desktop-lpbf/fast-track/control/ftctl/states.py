"""The supervisor's states and the transitions allowed between them. Any other transition raises."""
from __future__ import annotations

from enum import Enum


class S(str, Enum):
    IDLE = "IDLE"
    PURGE = "PURGE"            # argon at the purge flow until O2 < o2_start_ppm (heaters may start below heat_below_ppm)
    HEAT = "HEAT"              # plate and block to the set point, held ready_hold_s
    HOME = "HOME"              # home both stages hot, move to the build start
    READY = "READY"
    RECOAT_RETURN = "RECOAT_RETURN"   # hopper-blade back over the scanned layer, vibrator off
    PLATE_STEP = "PLATE_STEP"         # piston down one layer
    SPREAD = "SPREAD"                 # hopper-blade forward with the vibrator on, into the overflow
    SCAN = "SCAN"                     # the layer's list on the RTC5
    LOG = "LOG"
    DWELL = "DWELL"                   # wait for the plate to come back under setpoint + dwell_band_K
    HOLD = "HOLD"                     # wait for O2 or box air before a layer
    DONE = "DONE"
    COOLDOWN = "COOLDOWN"             # heaters off, argon at the idle flow, until the plate < open_plate_C
    VENT = "VENT"                     # argon off, slow air through the inlet filter until O2 >= 19.5 %
    SAFE_TO_OPEN = "SAFE_TO_OPEN"
    SAFE_STOP = "SAFE_STOP"           # laser off, list stopped, stages stopped, heaters per fault
    STOPPED = "STOPPED"


LAYER = {S.RECOAT_RETURN, S.PLATE_STEP, S.SPREAD, S.SCAN, S.LOG, S.DWELL, S.HOLD}
ALLOWED = {
    S.IDLE: {S.PURGE},
    S.PURGE: {S.HEAT},
    S.HEAT: {S.HOME},
    S.HOME: {S.READY},
    S.READY: {S.HOLD, S.PLATE_STEP, S.RECOAT_RETURN},
    S.HOLD: {S.RECOAT_RETURN, S.PLATE_STEP, S.HOLD},
    S.RECOAT_RETURN: {S.PLATE_STEP},
    S.PLATE_STEP: {S.SPREAD},
    S.SPREAD: {S.SCAN, S.DWELL},
    S.SCAN: {S.LOG},
    S.LOG: {S.DWELL, S.HOLD, S.RECOAT_RETURN, S.DONE},
    S.DWELL: {S.SCAN, S.HOLD, S.RECOAT_RETURN, S.DONE},
    S.DONE: {S.COOLDOWN, S.STOPPED},
    S.COOLDOWN: {S.VENT, S.STOPPED},
    S.VENT: {S.SAFE_TO_OPEN},
    S.SAFE_TO_OPEN: {S.STOPPED},
    S.SAFE_STOP: {S.STOPPED, S.COOLDOWN},
    S.STOPPED: set(),
}
# SAFE_STOP is reachable from every state except STOPPED.
for _s in S:
    if _s not in (S.STOPPED, S.SAFE_STOP):
        ALLOWED[_s] = ALLOWED[_s] | {S.SAFE_STOP}


class StateMachine:
    def __init__(self, clock, on_change=None):
        self.state = S.IDLE
        self.clock = clock
        self.history = [(clock.now(), None, S.IDLE, "start")]
        self.on_change = on_change

    def go(self, new: S, reason: str = "") -> None:
        if new not in ALLOWED[self.state]:
            raise RuntimeError(f"transition {self.state.value} -> {new.value} not allowed")
        old, self.state = self.state, new
        self.history.append((self.clock.now(), old, new, reason))
        if self.on_change:
            self.on_change(old, new, reason)

    def visited(self):
        return [h[2] for h in self.history]
