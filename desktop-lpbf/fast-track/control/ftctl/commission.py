"""Commissioning routines (README, arrival and commissioning checks). Each runs on the real machine or the simulation.

- focus_ladder: first light. Short lines at ~50 W on an anodised or bead-blasted plate, off the field centre (so a
  back-reflection travels back off-axis), one line per plate height (Edison round 2: first powered tests ~50 W).
- hot_piston_test: 10 full strokes at 200 C, then the stall margin: the stroke repeated at falling motor run current
  until it stalls (Zaber flag FS). Thrust scales with current, so the lowest current that still moves the piston
  gives the hot O-ring drag plus the plate's weight, against the X-VSR20A's 100 N continuous thrust.
- dose_spread_test: 20 dose-and-spread cycles with the real powder; each dose weighed; coefficient of variation < 15 %.
- chain_proof_test: operate each safety device alone and check the chain opens and re-arms (a stuck contact is only
  revealed by operating its own device alone; ftctl.interlock).
"""
from __future__ import annotations

import math
import statistics
from typing import Callable, List, Optional

import numpy as np

from .faults import Code, Fault
from .scanprog import Layer


def ladder_layer(P_W: float = 50.0, v_mm_s: float = 500.0, x0: float = 8.0, y: float = 0.0, length: float = 5.0,
                 index: int = 0) -> Layer:
    segs = np.array([[x0, y, x0 + length, y]])
    return Layer(index, 0.0, segs, np.array([P_W]), np.array([v_mm_s]), np.zeros(1, np.uint8), np.zeros(1, np.uint8))


def focus_ladder(sup, dz_mm=(-1.0, -0.5, 0.0, 0.5, 1.0), P_W: float = 50.0, v_mm_s: float = 500.0,
                 x0: float = 8.0, pitch: float = 1.5) -> List[dict]:
    """One 5 mm line per plate height, stacked in y, starting x0 mm off the field centre. The plate must be bare
    (no powder); the supervisor must be armed (READY)."""
    m, mo = sup.m, sup.cfg.motion
    out = []
    for i, dz in enumerate(dz_mm):
        sup.move(m.piston, mo.piston_build_start_mm + dz, mo.piston_step_speed)
        lay = ladder_layer(P_W, v_mm_s, x0, (i - (len(dz_mm) - 1) / 2) * pitch, index=i)
        planned = m.scan.load_layer(lay, sup.cfg.laser)
        sup.scanning = True
        m.scan.start()
        ok = sup.wait_until(lambda: not m.scan.busy(), planned["t_list"] + 1.0)
        sup.scanning = False
        if not ok:
            m.scan.stop()
            raise Fault(Code.RTC_ERROR, "ladder line overran", sup.clock.now())
        out.append(dict(dz_mm=dz, y_mm=float(lay.segs[0, 1]), P_W=P_W, energy_J=planned["energy_J"]))
    sup.move(m.piston, mo.piston_build_start_mm, mo.piston_step_speed)
    sup.log.event("commission", "FOCUS_LADDER", f"{len(out)} lines at {P_W:.0f} W, x0 = {x0} mm")
    return out


def hot_piston_test(sup, strokes: int = 10, stroke_mm: float = 15.0,
                    currents=(1.0, 0.6, 0.45, 0.35, 0.3, 0.25, 0.2, 0.15)) -> dict:
    """Run after HEAT (plate and block at 200 C). Returns stroke times and the stall margin."""
    m, mo = sup.m, sup.cfg.motion
    top, bottom = mo.piston_build_start_mm, mo.piston_build_start_mm - stroke_mm
    times = []
    for _ in range(strokes):
        times.append(sup.move(m.piston, bottom, mo.piston_step_speed))
        times.append(sup.move(m.piston, top, mo.piston_step_speed))
    lowest_ok = None
    for frac in currents:
        m.piston.set_run_current(frac)
        try:
            sup.move(m.piston, bottom, mo.piston_step_speed)
            sup.move(m.piston, top, mo.piston_step_speed)
            lowest_ok = frac
        except Fault:
            m.piston.clear_flags()
            break
    m.piston.set_run_current(1.0)
    thrust = getattr(m.piston, "thrust_N", 100.0)
    res = dict(strokes=strokes, stroke_mm=stroke_mm, mean_stroke_s=statistics.mean(times),
               spread_stroke_s=max(times) - min(times), lowest_current_that_moved=lowest_ok,
               drag_upper_bound_N=None if lowest_ok is None else round(lowest_ok * thrust, 1),
               margin=None if lowest_ok is None else round(1.0 / lowest_ok, 1))
    sup.log.event("commission", "HOT_PISTON", str(res))
    return res


def dose_spread_test(sup, weigh: Callable[[int], float], cycles: int = 20, cv_limit: float = 0.15) -> dict:
    """The hopper doses and spreads over the plate lowered by one layer each cycle; the operator (or a balance)
    weighs what reaches the overflow cup each cycle. Pass if the coefficient of variation is under cv_limit."""
    m, mo = sup.m, sup.cfg.motion
    doses = []
    for k in range(cycles):
        sup.move(m.recoater, mo.stage_x(mo.park_left_x), mo.return_speed)
        sup.set_out("VIBRATOR", True)
        try:
            sup.move(m.recoater, mo.stage_x(mo.park_right_x), mo.spread_speed)
        finally:
            sup.set_out("VIBRATOR", False)
        doses.append(float(weigh(k)))
    mean = statistics.mean(doses)
    cv = statistics.stdev(doses) / mean if mean > 0 else math.inf
    res = dict(cycles=cycles, mean_g=round(mean, 4), cv=round(cv, 3), passed=cv < cv_limit)
    sup.log.event("commission", "DOSE_SPREAD", str(res))
    return res


def chain_proof_test(sup, devices=("estop", "key", "lid", "beam_tube"),
                     operate: Optional[Callable[[str, bool], None]] = None, timeout: float = 120.0) -> List[dict]:
    """Daily: with the laser off, each device alone opens the chain (SAFETY_OK drops), then the chain re-arms.
    operate(device, open) is the operator (or the simulation)."""
    sup.m.laser.emission(False)
    sup.armed = False                    # the chain is about to open on purpose
    out = []
    for dev in devices:
        sup.log.event("prompt", f"PROOF_{dev.upper()}", f"open the {dev} alone")
        operate(dev, True)
        dropped = sup.wait_until(lambda: not sup.snap["SAFETY_OK"], timeout, poll=0.2)
        operate(dev, False)
        sup.ask("safety_reset", "close it again and press SAFETY RESET", lambda: sup.snap["SAFETY_OK"], timeout)
        out.append(dict(device=dev, opened_chain=dropped))
    return out
