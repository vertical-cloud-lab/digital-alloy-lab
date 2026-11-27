"""Simulated FT-1: one world model shared by simulated devices that implement ftctl.hw.interfaces.

Physics (lumped, parameters in ftctl.config with their sources):
- gas: well-mixed box of mixing_factor x box_volume_L; argon, vent air and leak air flow in, the mixture flows out;
  the leak is sized so the O2 floor at the build flow is Gas.floor_ppm; the analyzer is a first-order lag (T90);
- heat: plate and well block, each with its heaters (on only while K1 and K2 are closed), losses to the box air,
  and the argon gap between them; laser heat = absorptivity x the layer's energy, spread over the list time; box air
  rises 0.08 K per watt released into it (the study's fan case: 9-14 K for ~100-150 W);
- stages: trapezoidal moves at the commanded speed and acceleration;
- safety: the G9SE-201 (all inputs closed, then a reset), the laser's interlock, its power supply (START after the
  interlock closes) and EMON; the bimetal temperature switches open the chain at stray_switch_C;
- scan card: a list runs for its planned time (scanprog.layer_time) and emits a layer marker.
Fault injection: world.at(t, fn) or world.on_layer(k, fn), fn(world) sets the fault (see tests/test_faults.py).
"""
from __future__ import annotations

import math
import random
from typing import Callable, Dict, List, Optional, Set

from ..config import Config
from ..scanprog import layer_time
from .interfaces import ANALOG, INPUTS, OUTPUTS, Axis, Camera, HeaterZone, IoNode, Laser, Machine, ScanCard

NAN = float("nan")


class SimWorld:
    def __init__(self, cfg: Config, clock, timing: Optional[dict] = None, room_C: float = 22.0, seed: int = 1):
        self.cfg = cfg
        self.clock = clock
        clock.on_advance(self.advance)
        self.timing = timing
        self.rng = random.Random(seed)
        g, th = cfg.gas, cfg.thermal
        # gas
        self.o2 = g.air_o2_ppm
        self.o2_reading = g.analyzer_range_ppm     # trace cell, isolated in argon until its sample valve opens
        self.o2_pct_reading = g.air_o2_ppm / 1e4   # percent-range transmitter on the exhaust
        self.leak_Lpm = g.floor_ppm * g.build_flow_Lpm / (g.air_o2_ppm - g.floor_ppm)
        self.extra_leak_Lpm = 0.0
        self.room_o2_pct = 20.9
        self.argon_used_L = 0.0
        self.trace_cell_air_s = 0.0
        # heat
        self.room_C = room_C
        self.box_C = room_C
        self.Tp = self.Tb = room_C
        self.tc = {"plate": room_C, "block": room_C, "limit": room_C}
        self.window_C = self.tube_C = room_C
        self.tc_open: Set[str] = set()
        self.cn708_tripped = False
        self.cover_slide_fouling = 0.0     # fraction of the beam absorbed at the window (fault injection)
        self.stray_W = 0.0                 # stray beam power into the beam tube (fault injection)
        self.heater_stuck_on = set()       # SSR failed short (fault injection): 'plate' / 'block'
        self.box_fan_failed = False        # fault injection: the fan on the box stops
        self.loops_broken = set()          # fault injection: 4-20 mA loops reading below 3.6 mA
        self.box_extra_K = 0.0             # fault injection: extra box-air rise (e.g. a stage motor overheating)
        # safety chain
        self.estop_ok = True
        self.water_ok = True               # scan head cooling water flow switch
        self.lid_closed = True
        self.tube_closed = True
        self.key_on = True
        self.g9se = False
        self.g9se_needs_reset = True
        self.laser_ps = False
        self.emission = False
        self.laser_bits = 0                # injected STA bits (3 = back reflection, 1 = overheat, ...)
        self.laser_cfg = set()
        # scan card
        self.list_busy = False
        self.list_t0 = 0.0
        self.list_dur = 0.0
        self.list_E = 0.0
        self.list_layer = -1
        self.list_measured = None
        self.head = {"power": True, "temp": True, "pos_x": True, "pos_y": True}
        self.rtc_error = 0
        self.markers: List[tuple] = []     # (t, layer, edge) of DIGITAL OUT1
        self.laser_on_s = 0.0
        self.energy_in_plate_J = 0.0
        # devices registered later
        self.io: Optional[SimIo] = None
        self.zones: Dict[str, "SimHeater"] = {}
        self.axes: Dict[str, "SimAxis"] = {}
        self._timers: List[tuple] = []
        self._layer_hooks: Dict[int, List[Callable]] = {}
        self.operator_delay_s = 3.0

    # --------------------------------------------------------------- fault injection and the simulated operator
    def at(self, t: float, fn: Callable) -> None:
        self._timers.append((t, fn))
        self._timers.sort(key=lambda x: x[0])

    def on_layer(self, k: int, fn: Callable) -> None:
        self._layer_hooks.setdefault(k, []).append(fn)

    def operator(self, kind: str) -> None:
        """The simulated operator answers a prompt after operator_delay_s."""
        t = self.clock.now() + self.operator_delay_s
        if kind == "safety_reset":
            self.at(t, lambda w: w.press_reset())
        elif kind == "laser_start":
            self.at(t, lambda w: w.press_laser_start())

    def press_reset(self):
        if self.chain_closed():
            self.g9se = True
            self.g9se_needs_reset = False

    def press_laser_start(self):
        if self.g9se:
            self.laser_ps = True

    def chain_closed(self) -> bool:
        th = self.cfg.thermal
        switches_ok = self.tube_C < th.stray_switch_C and self.window_C < th.stray_switch_C
        return self.estop_ok and self.lid_closed and self.tube_closed and self.key_on and switches_ok

    # --------------------------------------------------------------- physics
    def advance(self, t0: float, t1: float) -> None:
        while self._timers and self._timers[0][0] <= t1:
            _, fn = self._timers.pop(0)
            fn(self)
        dt = t1 - t0
        if dt <= 0:
            return
        self._safety()
        self._scan(t0, t1)
        self._gas(dt)
        self._heat(t0, t1, dt)
        for ax in self.axes.values():
            ax._update(t1)

    def _safety(self):
        if not self.chain_closed():
            self.g9se = False
            self.g9se_needs_reset = True
        if not self.g9se:
            self.laser_ps = False
        if not self.laser_ps:
            self.emission = False

    def _scan(self, t0, t1):
        if self.list_busy and t1 >= self.list_t0 + self.list_dur:
            self.list_busy = False
            self.markers.append((self.list_t0 + self.list_dur, self.list_layer, 0))
            self.list_measured = self.list_dur

    def laser_power_now(self, t0, t1) -> float:
        """Mean laser power delivered between t0 and t1 (W)."""
        if not (self.list_busy and self.emission and self.list_dur > 0):
            return 0.0
        a, b = max(t0, self.list_t0), min(t1, self.list_t0 + self.list_dur)
        if b <= a:
            return 0.0
        return self.list_E / self.list_dur * (b - a) / (t1 - t0)

    def _gas(self, dt):
        g = self.cfg.gas
        io = self.io.out if self.io else {}
        room_ok = self.room_o2_pct >= g.room_alarm_pct        # the OX-6 relay is in series with both argon coils
        q_ar = (g.build_flow_Lpm if io.get("ARGON") else 0.0) + (g.idle_flow_Lpm if io.get("ARGON_LOW") else 0.0)
        q_ar = q_ar if room_ok else 0.0
        q_air = self.leak_Lpm + self.extra_leak_Lpm + (g.vent_flow_Lpm if io.get("VENT") else 0.0)
        q = q_ar + q_air
        self.argon_used_L += q_ar * dt / 60.0
        if q > 0:
            css = (q_ar * g.argon_o2_ppm + q_air * g.air_o2_ppm) / q
            k = q / 60.0 / (g.mixing_factor * g.box_volume_L)
            self.o2 = css + (self.o2 - css) * math.exp(-k * dt)
        if io.get("TRACE_SAMPLE"):
            tau = g.analyzer_t90_s / math.log(10.0)
            target = min(self.o2, g.analyzer_range_ppm)
            self.o2_reading += (target - self.o2_reading) * (1.0 - math.exp(-dt / tau))
            if self.o2 > 2 * g.analyzer_range_ppm:
                self.trace_cell_air_s += dt            # time the trace cell spent in near-air (shortens its life)
        tau = g.pct_t90_s / math.log(10.0)
        self.o2_pct_reading += (self.o2 / 1e4 - self.o2_pct_reading) * (1.0 - math.exp(-dt / tau))

    def _heat(self, t0, t1, dt):
        th = self.cfg.thermal
        k1 = bool(self.io and self.io.out.get("HEAT_EN")) and self.estop_ok
        k2 = not self.cn708_tripped
        P_las = self.laser_power_now(t0, t1)
        self.laser_on_s += dt if P_las > 0 else 0.0
        q_l = th.absorptivity * P_las * (1.0 - self.cover_slide_fouling)
        n = max(1, int(math.ceil(dt / 0.25)))
        h = dt / n
        for _ in range(n):
            Pp = Pb = 0.0
            for name, z in self.zones.items():
                u = 1.0 if name in self.heater_stuck_on else z._output()
                P = (th.plate_heater_W if name == "plate" else th.block_heater_W) * u if (k1 and k2) else 0.0
                if name == "plate":
                    Pp = P
                else:
                    Pb = P
            loss_p = th.plate_loss_WK * (self.Tp - self.box_C)
            loss_b = th.block_loss_WK * (self.Tb - self.box_C)
            gap = th.plate_block_WK * (self.Tp - self.Tb)
            self.Tp += h * (Pp + q_l - loss_p - gap) / th.plate_JK
            self.Tb += h * (Pb - loss_b + gap) / th.block_JK
            self.energy_in_plate_J += q_l * h
            # box air: 0.08 K/W released into it (study 3.5, fan case), 300 s time constant (estimate)
            into_air = loss_p + loss_b + (1.0 - th.absorptivity) * P_las
            # still air (fan failed): 32-46 K for the study's 102-147 W, ~0.31 K/W
            box_ss = self.room_C + (0.31 if self.box_fan_failed else 0.08) * into_air + self.box_extra_K
            self.box_C += (box_ss - self.box_C) * (1.0 - math.exp(-h / 300.0))
            # window ring: box air + 5 K + absorbed share of the beam (50 J/K, 0.5 W/K; estimate)
            win_ss = self.box_C + 5.0 + 2.0 * self.cover_slide_fouling * P_las
            self.window_C += (win_ss - self.window_C) * (1.0 - math.exp(-h / 100.0))
            tube_ss = self.room_C + 2.0 * self.stray_W
            self.tube_C += (tube_ss - self.tube_C) * (1.0 - math.exp(-h / 60.0))
            a = 1.0 - math.exp(-h / th.tc_tau_s)
            self.tc["plate"] += (self.Tp - self.tc["plate"]) * a
            self.tc["block"] += (self.Tb - self.tc["block"]) * a
            self.tc["limit"] += (self.Tp - self.tc["limit"]) * a
            if self.tc["limit"] > th.limit_C or "limit" in self.tc_open:
                self.cn708_tripped = True
            for z in self.zones.values():
                z._control(h)

    # --------------------------------------------------------------- scan card
    def start_list(self, layer_index: int, duration: float, energy: float):
        self.list_busy = True
        self.list_t0 = self.clock.now()
        self.list_dur = duration
        self.list_E = energy
        self.list_layer = layer_index
        self.markers.append((self.list_t0, layer_index, 1))
        for fn in self._layer_hooks.pop(layer_index, []):
            fn(self)

    def stop_list(self):
        if self.list_busy:
            self.list_busy = False
            self.markers.append((self.clock.now(), self.list_layer, 0))
            self.list_measured = self.clock.now() - self.list_t0


class SimScan(ScanCard):
    def __init__(self, world: SimWorld, timing: dict):
        self.w = world
        self.timing = timing
        self.planned = None
        self.opened = False

    def open(self):
        self.opened = True

    def load_layer(self, layer, laser_cfg=None) -> dict:
        lt = layer_time(layer, self.timing)
        self.planned = (layer.index, lt)
        return lt

    def start(self):
        k, lt = self.planned
        self.w.start_list(k, lt["t_list"], lt["energy_J"])

    def busy(self) -> bool:
        return self.w.list_busy

    def stop(self):
        self.w.stop_list()

    def head_status(self):
        return dict(self.w.head)

    def last_error(self) -> int:
        return self.w.rtc_error

    def list_time(self):
        return self.w.list_measured


class SimLaser(Laser):
    def __init__(self, world: SimWorld):
        self.w = world

    def open(self):
        pass

    def configure(self):
        self.w.laser_cfg = {"EEC", "EMOD", "DLE", "ABF"}

    def emission(self, on: bool):
        self.w.emission = bool(on and self.w.laser_ps)

    def status(self) -> int:
        w = self.w
        s = w.laser_bits
        s |= (1 << 2) if w.emission else 0
        s |= (1 << 4) if "EEC" in w.laser_cfg else 0
        s |= (1 << 12) if "EMOD" in w.laser_cfg else 0
        s |= (1 << 11) if not w.laser_ps else 0
        s |= 1 << 21                                   # keyswitch in REM
        return s

    def reset_errors(self):
        self.w.laser_bits = 0


class SimAxis(Axis):
    def __init__(self, world: SimWorld, name: str, travel: float, vmax: float, amax: float, pos: float = 0.0,
                 thrust_N: float = 100.0, load_N: float = 0.0):
        self.w = world
        self.thrust_N = thrust_N          # continuous thrust at full run current (Zaber specs)
        self.load_N = load_N              # drag + weight it must overcome (estimate)
        self.run_current = 1.0
        self.name = name
        self.travel = travel
        self.vmax = vmax
        self.amax = amax
        self.pos = pos
        self.homed = False
        self.move = None        # (t0, x0, x1, v, a, T)
        self._flags: Set[str] = {"WR"}
        self.stall_next = False
        world.axes[name] = self

    @staticmethod
    def _duration(d, v, a):
        if d <= 0:
            return 0.0
        return d / v + v / a if d >= v * v / a else 2.0 * math.sqrt(d / a)

    def _pos_at(self, t):
        t0, x0, x1, v, a, T = self.move
        d = abs(x1 - x0)
        s = 1.0 if x1 >= x0 else -1.0
        tau = min(max(t - t0, 0.0), T)
        if d >= v * v / a:
            ta = v / a
            if tau < ta:
                dd = 0.5 * a * tau * tau
            elif tau < T - ta:
                dd = 0.5 * a * ta * ta + v * (tau - ta)
            else:
                r = T - tau
                dd = d - 0.5 * a * r * r
        else:
            tp = T / 2.0
            dd = 0.5 * a * tau * tau if tau < tp else d - 0.5 * a * (T - tau) ** 2
        return x0 + s * dd

    def _update(self, t):
        if self.move:
            self.pos = self._pos_at(t)
            if t >= self.move[0] + self.move[5]:
                self.pos = self.move[2]
                self.move = None

    def home(self, wait=True):
        self.move_abs(0.0, self.vmax / 2, self.amax, wait=wait, _homing=True)
        self.homed = True
        self._flags.discard("WR")

    def move_abs(self, pos_mm, speed=None, accel=None, wait=False, _homing=False):
        if not self.homed and not _homing:
            raise RuntimeError(f"{self.name}: not homed")
        if any(f.startswith("F") for f in self._flags):
            raise RuntimeError(f"{self.name}: fault {sorted(self._flags)}")
        pos_mm = min(max(pos_mm, 0.0), self.travel)
        v = min(speed or self.vmax, self.vmax)
        a = accel or self.amax
        x1 = pos_mm
        if self.thrust_N * self.run_current < self.load_N:     # not enough thrust: stalls where it stands
            self.w.at(self.w.clock.now() + 0.05, lambda w: self._flags.add("FS"))
            self.move = (self.w.clock.now(), self.pos, self.pos, v, a, 0.05)
            return
        if self.stall_next:                     # stalls half way and sets FS (STALLED_AND_STOPPED)
            x1 = self.pos + 0.5 * (pos_mm - self.pos)
        T = self._duration(abs(x1 - self.pos), v, a)
        self.move = (self.w.clock.now(), self.pos, x1, v, a, T)
        if self.stall_next:
            stall_t = self.move[0] + T
            self.w.at(stall_t, lambda w: self._flags.add("FS"))
            self.stall_next = False
        if wait:
            while self.busy():
                self.w.clock.sleep(0.05)

    def position(self):
        return self.pos

    def busy(self):
        return self.move is not None

    def stop(self):
        self._update(self.w.clock.now())
        self.move = None

    def flags(self):
        return set(self._flags)

    def clear_flags(self):
        f = set(self._flags)
        self._flags = {x for x in self._flags if not x.startswith("F")}
        return f

    def set_run_current(self, fraction: float) -> None:
        self.run_current = fraction

    def planned_time(self, target, speed=None, accel=None):
        return self._duration(abs(target - self.pos), min(speed or self.vmax, self.vmax), accel or self.amax)


class SimHeater(HeaterZone):
    """A stand-alone PID controller (PI with anti-windup) on its own thermocouple, driving an SSR."""

    def __init__(self, world: SimWorld, name: str, kp: float, ti: float):
        self.w = world
        self.name = name
        self.kp, self.ti = kp, ti
        self.sv = 0.0
        self.running = False
        self.integ = 0.0
        self.u = 0.0
        world.zones[name] = self

    def _control(self, h):
        if not self.running or self.name in self.w.tc_open:
            self.u = 0.0                       # sensor-break action: output off
            return
        e = self.sv - self.w.tc[self.name]
        u = self.kp * e + self.integ
        if 0.0 < u < 1.0 or (u >= 1.0 and e < 0) or (u <= 0.0 and e > 0):
            self.integ += self.kp * e * h / self.ti
        self.u = min(max(u, 0.0), 1.0)

    def _output(self):
        return self.u

    def pv(self):
        return NAN if self.name in self.w.tc_open else self.w.tc[self.name]

    def set_sv(self, celsius):
        self.sv = celsius

    def run(self, on):
        self.running = bool(on)
        if not on:
            self.integ = 0.0

    def output_pct(self):
        return 100.0 * self.u


class SimIo(IoNode):
    def __init__(self, world: SimWorld):
        self.w = world
        self.out = {k: False for k in OUTPUTS}
        self.link_ok = True
        world.io = self

    def _check(self):
        if not self.link_ok:
            raise ConnectionError("Pi I/O node not answering")

    def set(self, name, on):
        self._check()
        self.out[name] = bool(on)

    def get(self, name):
        self._check()
        w = self.w
        return {
            "SAFETY_OK": w.g9se,
            "WATER_OK": w.water_ok,
            "LID_CLOSED": w.lid_closed,
            "LASER_PS_ACTIVE": w.laser_ps,
            "LASER_EMISSION": w.emission,
            "LASER_READY": not (w.laser_bits & ((1 << 1) | (1 << 3) | (1 << 29))),
            "LIMIT_OK": not w.cn708_tripped,
            "ROOM_O2_OK": w.room_o2_pct >= w.cfg.gas.room_alarm_pct,
            "K1_ON": self.out["HEAT_EN"] and w.estop_ok,
        }[name]

    def temps(self):
        self._check()
        w = self.w
        t = {"window": w.window_C, "beam_tube": w.tube_C, "box_air": w.box_C, "stage": w.box_C + 3.0}
        for k in list(t):
            if k in w.tc_open:
                t[k] = NAN
        return t

    def analog(self):
        self._check()
        w = self.w
        nan = float("nan")
        return {"o2_ppm": nan if "o2_ppm" in w.loops_broken else min(w.o2_reading, w.cfg.gas.analyzer_range_ppm),
                "o2_pct": nan if "o2_pct" in w.loops_broken else w.o2_pct_reading,
                "room_o2_pct": nan if "room_o2_pct" in w.loops_broken else w.room_o2_pct}

class SimCamera(Camera):
    def __init__(self, world):
        self.w = world
        self.shots = []

    def capture(self, tag, layer):
        self.shots.append((self.w.clock.now(), tag, layer))
        return None


def make_sim_machine(cfg: Config, clock, timing: dict, seed: int = 1) -> Machine:
    w = SimWorld(cfg, clock, timing, seed=seed)
    m = cfg.motion
    th = cfg.thermal
    io = SimIo(w)
    machine = Machine(
        scan=SimScan(w, timing),
        laser=SimLaser(w),
        # X-VSR20A: 100 N continuous; load = hot O-ring drag ~20 N (estimate) + plate, disc and rod ~3 N
        piston=SimAxis(w, "piston", m.piston_travel_mm, 48.0, m.piston_accel, pos=8.0, thrust_N=100.0, load_N=23.0),
        # X-LSM100B: 25 N continuous; load = blade and hopper drag ~5 N (estimate)
        recoater=SimAxis(w, "recoater", m.recoater_travel_mm, 104.0, m.recoater_accel, pos=60.0, thrust_N=25.0,
                         load_N=5.0),
        plate=SimHeater(w, "plate", *th.pid_plate),
        block=SimHeater(w, "block", *th.pid_block),
        io=io,
        camera=SimCamera(w) if cfg.camera else None,
        world=w,
    )
    return machine


__all__ = ["SimWorld", "make_sim_machine", "ANALOG", "INPUTS", "OUTPUTS"]
