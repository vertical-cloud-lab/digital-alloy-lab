"""The build supervisor: start-up (purge, heat, home, arm), the layer loop, the end of a build, faults and the safe stop.

Layer loop (study 3.3: scan, return the hopper over the scanned layer, lower the plate, spread forward):
  preflight (interlocks, laser status, O2 < o2_start_ppm, box air)  -> HOLD if needed
  RECOAT_RETURN (not on the first layer) -> PLATE_STEP -> SPREAD (vibrator on) -> camera 'powder'
  SCAN (the layer's RTC5 list; O2, laser STA, scanner status polled throughout) -> camera 'scanned'
  LOG -> DWELL while the plate is above setpoint + dwell_band_K -> next layer
"""
from __future__ import annotations

import math
from typing import Callable, Iterable, Optional

from .clock import Clock
from .config import Config
from .faults import Code, Fault
from .hw.interfaces import Machine
from .logger import BuildLog
from .scanprog import ScanProgram
from .states import S, StateMachine

# IPG YLR STA bits (YLR-series user guide, interface commands): faults the supervisor acts on
STA_FAULT_BITS = {1: "overheat", 6: "module disconnected", 19: "power supply failure", 24: "low temperature",
                  25: "power supply failure (2)", 29: "critical error", 30: "optical interlock active",
                  31: "average power too high"}
STA_BACK_REFLECTION = 3
STA_EMISSION = 2


def trapezoid_time(d: float, v: float, a: float) -> float:
    if d <= 0:
        return 0.0
    return d / v + v / a if d >= v * v / a else 2.0 * math.sqrt(d / a)


class Supervisor:
    def __init__(self, machine: Machine, cfg: Config, program: ScanProgram, log: BuildLog, clock: Clock,
                 operator: Optional[Callable[[str], None]] = None):
        self.m = machine
        self.cfg = cfg
        self.prog = program
        self.log = log
        self.clock = clock
        self.sm = StateMachine(clock, on_change=lambda a, b, r: log.event("state", b.value, r))
        if operator is None:
            operator = machine.world.operator if machine.world is not None else self._console_operator
        self.operator = operator
        self.armed = False
        self.heating = False
        self.scanning = False
        self.snap: dict = {}
        self.outputs = {}
        self.stop_request: Optional[str] = None
        self.fault: Optional[Fault] = None
        self.warned = set()
        self.row: Optional[dict] = None
        self.times = {}
        self._t_sample = -1e9
        self._t_sta = -1e9
        self._t_head = -1e9
        self._t_flags = -1e9
        self._t_pv = -1e9
        self._pv = {}
        self._ready_since = None
        log.attrs["config"] = cfg.to_json()
        log.attrs["program"] = program.source

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _console_operator(kind: str) -> None:
        print(f"[operator] {kind}: see the prompt in the log")

    def set_out(self, name: str, on: bool) -> None:
        self.m.io.set(name, on)
        self.outputs[name] = bool(on)

    def ask(self, kind: str, message: str, cond: Callable[[], bool], timeout: float) -> None:
        self.log.event("prompt", kind, message)
        self.operator(kind)
        if not self.wait_until(cond, timeout, poll=0.5):
            raise Fault(Code.INTERLOCK_OPEN, f"operator prompt '{kind}' not answered in {timeout:.0f} s")

    def poll(self) -> dict:
        t = self.clock.now()
        try:
            s = dict(self.m.io.snapshot())
        except Exception as e:                                   # noqa: BLE001
            raise Fault(Code.IO_LINK_LOST, f"Pi I/O node: {e}", t)
        if t - self._t_pv >= 0.25 or not self._pv:
            self._t_pv = t
            self._pv = dict(plate_C=self.m.plate.pv(), block_C=self.m.block.pv())
        s.update(self._pv)
        self.snap = s
        if t - self._t_sample >= self.cfg.sample_s:
            self._sample(t, s)
        self._check(t, s)
        return s

    def _sample(self, t, s):
        self._t_sample = t
        self.log.sample(dict(
            t=t, state=self.sm.state.value, plate_C=s["plate_C"], block_C=s["block_C"],
            plate_out_pct=self.m.plate.output_pct(), block_out_pct=self.m.block.output_pct(), o2_ppm=s["o2_ppm"],
            room_o2_pct=s["room_o2_pct"], box_air_C=s["box_air"], window_C=s["window"], beam_tube_C=s["beam_tube"],
            stage_C=s["stage"], piston_mm=self.m.piston.position(), recoater_mm=self.m.recoater.position(),
            safety_ok=float(s["SAFETY_OK"]), laser_ps=float(s["LASER_PS_ACTIVE"]),
            laser_emission=float(s["LASER_EMISSION"]), limit_ok=float(s["LIMIT_OK"]), k1_on=float(s["K1_ON"]),
            argon=float(self.outputs.get("ARGON", False)), vibrator=float(self.outputs.get("VIBRATOR", False))))

    def _warn(self, key, text):
        if key not in self.warned:
            self.warned.add(key)
            self.log.event("warning", key, text)

    def _check(self, t, s):
        th, g = self.cfg.thermal, self.cfg.gas
        if self.stop_request == "abort":
            raise Fault(Code.OPERATOR_STOP, "abort requested", t)
        if not s["ROOM_O2_OK"] or s["room_o2_pct"] < g.room_alarm_pct:
            raise Fault(Code.ROOM_O2_LOW, f"room O2 {s['room_o2_pct']:.1f} %", t)
        for k in ("plate_C", "block_C", "window", "beam_tube", "box_air", "stage"):
            if s[k] is None or math.isnan(s[k]):
                raise Fault(Code.TC_OPEN, f"thermocouple '{k}' open", t)
        hot = max(s["plate_C"], s["block_C"])
        if hot > th.soft_limit_C:
            raise Fault(Code.PLATE_OVERTEMP, f"plate {s['plate_C']:.1f} C, block {s['block_C']:.1f} C", t)
        if self.heating and not s["LIMIT_OK"]:
            raise Fault(Code.LIMIT_TRIPPED, "CN708 limit opened K2", t)
        if s["window"] > th.window_fault_C:
            raise Fault(Code.WINDOW_HOT, f"window ring {s['window']:.1f} C: check the cover slide", t)
        if s["window"] > th.window_warn_C:
            self._warn("WINDOW_WARM", f"window ring {s['window']:.1f} C")
        if s["beam_tube"] > th.beam_tube_fault_C:
            raise Fault(Code.STRAY_BEAM, f"beam tube {s['beam_tube']:.1f} C", t)
        if s["box_air"] > th.box_air_fault_C:
            raise Fault(Code.BOX_AIR_HOT, f"box air {s['box_air']:.1f} C (stages rated 50 C)", t)
        if self.armed:
            if not s["SAFETY_OK"]:
                raise Fault(Code.INTERLOCK_OPEN, "safety relay open (lid, beam tube, E-stop, key or temperature "
                                                 "switch)", t)
            if not s["LASER_PS_ACTIVE"]:
                raise Fault(Code.LASER_FAULT, "laser power supply dropped with the interlock closed", t)
            period = 0.2 if self.scanning else 1.0
            if not s["LASER_READY"] or t - self._t_sta >= period:
                self._t_sta = t
                self._check_sta(t, self.m.laser.status(), ready=s["LASER_READY"])
        if self.scanning:
            if s["o2_ppm"] > g.o2_trip_ppm:
                raise Fault(Code.O2_HIGH, f"O2 {s['o2_ppm']:.0f} ppm during the scan", t)
            if t - self._t_head >= 0.2:
                self._t_head = t
                hs = self.m.scan.head_status()
                if not (hs.get("power") and hs.get("temp")):
                    raise Fault(Code.SCANNER_FAULT, f"scan head status {hs}", t)
                err = self.m.scan.last_error()
                if err:
                    raise Fault(Code.RTC_ERROR, f"RTC5 get_last_error = {err}", t)
        if t - self._t_flags >= 0.5:
            self._t_flags = t
            self._check_axes(t)

    def _check_sta(self, t, sta: int, ready: bool = True):
        if sta & (1 << STA_BACK_REFLECTION):
            raise Fault(Code.BACK_REFLECTION, f"laser STA {sta:#010x}: high back reflection", t, dict(sta=sta))
        bad = [name for b, name in STA_FAULT_BITS.items() if sta & (1 << b)]
        if bad or not ready:
            raise Fault(Code.LASER_FAULT, f"laser STA {sta:#010x}: {', '.join(bad) or 'Error/Ready low'}", t,
                        dict(sta=sta))

    def _check_axes(self, t):
        for ax in (self.m.piston, self.m.recoater):
            fl = ax.flags()
            bad = sorted(f for f in fl if f.startswith("F"))
            if bad:
                raise Fault(Code.STAGE_FAULT, f"{ax.name}: Zaber flags {bad}", t, dict(flags=bad))

    def wait_until(self, cond: Callable[[], bool], timeout: float, poll: Optional[float] = None) -> bool:
        t_end = self.clock.now() + timeout
        while True:
            self.poll()
            if cond():
                return True
            if self.clock.now() >= t_end:
                return False
            self.clock.sleep(poll or self.cfg.poll_s)

    def move(self, ax, target: float, speed: Optional[float] = None, accel: Optional[float] = None) -> float:
        mo = self.cfg.motion
        t0 = self.clock.now()
        v = speed or getattr(ax, "vmax", 50.0)
        a = accel or getattr(ax, "amax", 500.0)
        planned = trapezoid_time(abs(target - ax.position()), v, a)
        ax.move_abs(target, speed, accel, wait=False)
        if not self.wait_until(lambda: not ax.busy(), planned + mo.move_timeout_margin_s):
            ax.stop()
            raise Fault(Code.STAGE_FAULT, f"{ax.name}: move to {target:.3f} mm overran {planned:.2f} s",
                        self.clock.now())
        self._check_axes(self.clock.now())
        err = ax.position() - target
        if abs(err) > 0.05:
            raise Fault(Code.STAGE_FAULT, f"{ax.name}: at {ax.position():.3f} mm, wanted {target:.3f} mm",
                        self.clock.now())
        return self.clock.now() - t0

    def heaters(self, on: bool) -> None:
        sp = self.cfg.thermal.setpoint_C
        for z in (self.m.plate, self.m.block):
            z.set_sv(sp)
            z.run(on)
        self.set_out("HEAT_EN", on)
        self.heating = on
        self.log.event("heaters", "ON" if on else "OFF")

    # ------------------------------------------------------------------ start-up
    def connect(self) -> None:
        self.m.scan.open()
        self.m.laser.open()
        for name in ("ARGON", "ARGON_LOW", "VENT", "VIBRATOR", "HEAT_EN", "LEDS", "BEACON"):
            self.set_out(name, False)
        self.log.event("info", "CONNECTED", "scan card, laser, I/O node")

    def startup(self) -> None:
        g, th, mo = self.cfg.gas, self.cfg.thermal, self.cfg.motion
        t0 = self.clock.now()
        self.sm.go(S.PURGE, f"argon on, purge to {g.o2_start_ppm:.0f} ppm")
        self.set_out("ARGON", True)

        def purged():
            o2 = self.snap["o2_ppm"]
            if self.cfg.overlap_heat_with_purge and not self.heating and o2 < g.heat_below_ppm:
                self.heaters(True)
            return o2 < g.o2_start_ppm

        if not self.wait_until(purged, g.purge_timeout_s, poll=0.5):
            raise Fault(Code.O2_TIMEOUT, f"purge did not reach {g.o2_start_ppm:.0f} ppm in {g.purge_timeout_s:.0f} s "
                                         f"(at {self.snap['o2_ppm']:.0f} ppm)", self.clock.now())
        self.times["purge_s"] = self.clock.now() - t0
        t1 = self.clock.now()
        self.sm.go(S.HEAT, f"plate and block to {th.setpoint_C:.0f} C")
        if not self.heating:
            self.heaters(True)

        def hot():
            s = self.snap
            ok = abs(s["plate_C"] - th.setpoint_C) <= th.ready_band_K and abs(s["block_C"] - th.setpoint_C) <= th.ready_band_K
            now = self.clock.now()
            if not ok:
                self._ready_since = None
                return False
            if self._ready_since is None:
                self._ready_since = now
            return now - self._ready_since >= th.ready_hold_s

        if not self.wait_until(hot, th.heat_timeout_s, poll=0.5):
            raise Fault(Code.HEAT_TIMEOUT, f"plate {self.snap['plate_C']:.1f} C, block {self.snap['block_C']:.1f} C "
                                           f"after {th.heat_timeout_s:.0f} s", self.clock.now())
        self.times["heat_s"] = self.clock.now() - t1
        self.times["ready_from_start_s"] = self.clock.now() - t0
        t2 = self.clock.now()
        self.sm.go(S.HOME, "home both stages hot, then to the build start")
        self.m.piston.home(wait=False)
        self.m.recoater.home(wait=False)
        if not self.wait_until(lambda: not (self.m.piston.busy() or self.m.recoater.busy()), 60.0):
            raise Fault(Code.STAGE_FAULT, "homing overran 60 s", self.clock.now())
        self.move(self.m.recoater, mo.stage_x(mo.park_left_x))
        self.move(self.m.piston, mo.piston_build_start_mm, mo.piston_step_speed)
        self.times["home_s"] = self.clock.now() - t2
        self.arm()
        self.sm.go(S.READY, "armed")
        self.times["startup_s"] = self.clock.now() - t0

    def arm(self) -> None:
        """Operator closes the chain (SAFETY RESET) and starts the laser's supply (LASER START); then EMON."""
        if not self.snap.get("SAFETY_OK"):
            self.ask("safety_reset", "Close the lid, turn the key on, press SAFETY RESET",
                     lambda: self.snap["SAFETY_OK"], 600.0)
        if not self.snap.get("LASER_PS_ACTIVE"):
            self.ask("laser_start", "Press LASER START", lambda: self.snap["LASER_PS_ACTIVE"], 600.0)
        self.m.laser.configure()
        self.m.laser.emission(True)
        if not self.wait_until(lambda: bool(self.m.laser.status() & (1 << STA_EMISSION)), 5.0, poll=0.2):
            raise Fault(Code.LASER_FAULT, f"EMON not acknowledged (STA {self.m.laser.status():#010x})",
                        self.clock.now())
        hs = self.m.scan.head_status()
        if not (hs.get("power") and hs.get("temp")):
            raise Fault(Code.SCANNER_FAULT, f"scan head status {hs}", self.clock.now())
        self.armed = True
        self.log.event("armed", "EMON", "emission enabled; the RTC5's LASERON gates the beam")

    # ------------------------------------------------------------------ the layer loop
    def preflight(self) -> float:
        g, th = self.cfg.gas, self.cfg.thermal
        self.poll()
        s = self.snap
        if s["o2_ppm"] < g.o2_start_ppm and s["box_air"] < th.box_air_hold_C:
            return 0.0
        t0 = self.clock.now()
        self.sm.go(S.HOLD, f"O2 {s['o2_ppm']:.0f} ppm, box air {s['box_air']:.1f} C")
        ok = self.wait_until(lambda: self.snap["o2_ppm"] < g.o2_start_ppm and self.snap["box_air"] < th.box_air_resume_C,
                             g.o2_hold_timeout_s, poll=0.5)
        if not ok:
            code = Code.O2_TIMEOUT if self.snap["o2_ppm"] >= g.o2_start_ppm else Code.BOX_AIR_HOT
            raise Fault(code, f"hold timed out: O2 {self.snap['o2_ppm']:.0f} ppm, box air {self.snap['box_air']:.1f} C",
                        self.clock.now())
        return self.clock.now() - t0

    def build(self, layers: Iterable[int]) -> None:
        mo, th = self.cfg.motion, self.cfg.thermal
        lm = self.prog.layer_mm
        first = True
        for k in layers:
            if self.stop_request == "graceful":
                raise Fault(Code.OPERATOR_STOP, "graceful stop between layers", self.clock.now())
            layer = self.prog.layer(k)
            z = mo.piston_build_start_mm - (k + 1) * lm
            if z < mo.piston_min_mm:
                raise Fault(Code.STAGE_FAULT, f"layer {k}: piston at {z:.3f} mm is out of travel", self.clock.now())
            row = self.row = dict(layer=k, z_mm=(k + 1) * lm, t_start=self.clock.now(), complete=0.0,
                                  n_vectors=len(layer))
            row["hold_s"] = self.preflight()
            t_rc = self.clock.now()
            if not first:
                self.sm.go(S.RECOAT_RETURN)
                self.move(self.m.recoater, mo.stage_x(mo.park_left_x), mo.return_speed)
            self.sm.go(S.PLATE_STEP, f"z = {z:.3f} mm")
            self.move(self.m.piston, z, mo.piston_step_speed)
            self.clock.sleep(mo.settle_s)
            self.sm.go(S.SPREAD)
            self.set_out("VIBRATOR", True)
            try:
                self.move(self.m.recoater, mo.stage_x(mo.park_right_x), mo.spread_speed)
            finally:
                self.set_out("VIBRATOR", False)
            row["t_recoat_end"] = self.clock.now()
            row["recoat_s"] = row["t_recoat_end"] - t_rc
            self._photo("powder", k)
            row["dwell_s"] = self.dwell("before the scan")
            self.sm.go(S.SCAN)
            planned = self.m.scan.load_layer(layer, self.cfg.laser)
            row["planned_scan_s"] = planned["t_list"]
            row["energy_J"] = planned["energy_J"]
            row["plate_C_scan_start"] = self.snap["plate_C"]
            row["o2_ppm_scan_start"] = self.snap["o2_ppm"]
            self.scanning = True
            row["t_scan_start"] = self.clock.now()
            self.m.scan.start()
            self.log.event("list", "START", f"layer {k}", planned_s=planned["t_list"])
            ok = self.wait_until(lambda: not self.m.scan.busy(), planned["t_list"] + 1.0)
            self.scanning = False
            if not ok:
                self.m.scan.stop()
                raise Fault(Code.RTC_ERROR, f"layer {k}: list still busy {planned['t_list'] + 1.0:.2f} s after start",
                            self.clock.now())
            row["t_scan_end"] = self.clock.now()
            row["scan_s"] = row["t_scan_end"] - row["t_scan_start"]
            self.log.event("list", "END", f"layer {k}", card_s=self.m.scan.list_time())
            row["plate_C_scan_end"] = self.snap["plate_C"]
            self._photo("scanned", k)
            self.sm.go(S.LOG)
            row["complete"] = 1.0
            row["dwell_s"] += self.dwell("after the scan")
            row["t_end"] = self.clock.now()
            self.log.layer(row)
            self.row = None
            first = False
        self.sm.go(S.DONE, "all layers scanned")

    def dwell(self, why: str) -> float:
        """Wait until the plate is back under setpoint + dwell_band_K. Checked after each scan and again just before
        the next one (the thermocouple lags, so the reading can still be rising after the scan)."""
        th = self.cfg.thermal
        band = th.setpoint_C + th.dwell_band_K
        t0 = self.clock.now()
        self.poll()
        if self.snap["plate_C"] <= band:
            return 0.0
        self.sm.go(S.DWELL, f"plate {self.snap['plate_C']:.1f} C, {why}")
        if not self.wait_until(lambda: self.snap["plate_C"] <= band, th.dwell_max_s, poll=0.5):
            raise Fault(Code.DWELL_TIMEOUT, f"plate {self.snap['plate_C']:.1f} C after {th.dwell_max_s:.0f} s",
                        self.clock.now())
        return self.clock.now() - t0

    def _photo(self, tag, k):
        if self.m.camera is None:
            return
        self.set_out("LEDS", True)
        self.m.camera.capture(tag, k)
        self.set_out("LEDS", False)

    # ------------------------------------------------------------------ end of a build
    def finish(self) -> None:
        g, th = self.cfg.gas, self.cfg.thermal
        self.m.laser.emission(False)
        self.armed = False
        self.log.event("armed", "EMOFF", "build done")
        if not self.cfg.vent_after_build:
            self.sm.go(S.STOPPED, "no vent requested")
            return
        t0 = self.clock.now()
        self.sm.go(S.COOLDOWN, f"heaters off, argon at the idle flow until the plate < {th.open_plate_C:.0f} C")
        self.heaters(False)
        self.set_out("ARGON_LOW", True)
        self.set_out("ARGON", False)
        if not self.wait_until(lambda: max(self.snap["plate_C"], self.snap["block_C"]) < th.open_plate_C, 4 * 3600.0,
                               poll=2.0):
            raise Fault(Code.PLATE_OVERTEMP, "plate still hot after 4 h of cooling", self.clock.now())
        self.times["cooldown_s"] = self.clock.now() - t0
        t1 = self.clock.now()
        self.sm.go(S.VENT, "argon off, air in slowly through the inlet filter")
        self.set_out("ARGON_LOW", False)
        self.set_out("VENT", True)
        if not self.wait_until(lambda: self.snap["o2_ppm"] >= g.open_o2_ppm, 3 * 3600.0, poll=2.0):
            raise Fault(Code.O2_TIMEOUT, "vent did not reach 19.5 % O2 in 3 h", self.clock.now())
        self.times["vent_s"] = self.clock.now() - t1
        self.sm.go(S.SAFE_TO_OPEN, f"O2 {self.snap['o2_ppm'] / 1e4:.1f} %, plate {self.snap['plate_C']:.0f} C")
        self.set_out("BEACON", True)
        self.sm.go(S.STOPPED)

    # ------------------------------------------------------------------ faults
    def safe_stop(self, fault: Fault) -> None:
        self.fault = fault
        self.log.event("fault", fault.code.value, fault.message, **fault.data)
        self.scanning = False
        steps = [("scan.stop", self.m.scan.stop), ("laser.emission(False)", lambda: self.m.laser.emission(False)),
                 ("piston.stop", self.m.piston.stop), ("recoater.stop", self.m.recoater.stop),
                 ("vibrator off", lambda: self.set_out("VIBRATOR", False))]
        if fault.code != Code.IO_LINK_LOST:
            steps.append(("heaters off", lambda: self.heaters(False)))
        if fault.code == Code.ROOM_O2_LOW:
            steps += [("argon off", lambda: self.set_out("ARGON", False)),
                      ("argon low off", lambda: self.set_out("ARGON_LOW", False))]
        for name, fn in steps:
            try:
                fn()
            except Exception as e:                               # noqa: BLE001
                self.log.event("error", "SAFE_STOP_STEP", f"{name}: {e}")
        self.armed = False
        if self.row is not None:
            self.row["t_end"] = self.clock.now()
            self.log.layer(self.row)
            self.row = None
        if self.sm.state not in (S.SAFE_STOP, S.STOPPED):
            self.sm.go(S.SAFE_STOP, fault.code.value)
        if self.sm.state != S.STOPPED:
            self.sm.go(S.STOPPED, "safe")

    def request_stop(self, graceful: bool = True) -> None:
        self.stop_request = "graceful" if graceful else "abort"

    # ------------------------------------------------------------------ the whole run
    def run(self, layers: Optional[Iterable[int]] = None, startup: bool = True, finish: bool = True) -> dict:
        layers = list(range(self.prog.n_layers) if layers is None else layers)
        t0 = self.clock.now()
        try:
            self.connect()
            if startup:
                self.startup()
            t_b = self.clock.now()
            self.build(layers)
            self.times["build_s"] = self.clock.now() - t_b
            if finish:
                self.finish()
            else:
                self.m.laser.emission(False)
                self.armed = False
                self.sm.go(S.STOPPED, "left hot and under argon")
        except Fault as f:
            f.t = f.t or self.clock.now()
            self.safe_stop(f)
        except KeyboardInterrupt:
            self.safe_stop(Fault(Code.OPERATOR_STOP, "Ctrl-C", self.clock.now()))
        except Exception as e:                                   # noqa: BLE001
            self.safe_stop(Fault(Code.INTERNAL_ERROR, f"unexpected: {e!r}", self.clock.now()))
        self.times["total_s"] = self.clock.now() - t0
        return self.log.close(self.summary(layers))

    def summary(self, layers) -> dict:
        rows = [r for r in self.log.layers if r.get("complete")]
        w = self.m.world

        def stat(key):
            v = [r[key] for r in rows if key in r]
            return dict(mean=sum(v) / len(v), min=min(v), max=max(v), total=sum(v)) if v else None

        periods = [b["t_start"] - a["t_start"] for a, b in zip(rows, rows[1:])]
        out = dict(
            result="fault" if self.fault else "complete",
            fault=None if not self.fault else dict(code=self.fault.code.value, message=self.fault.message,
                                                     t=self.fault.t),
            final_state=self.sm.state.value,
            program=self.prog.source,
            layers_requested=len(list(layers)),
            layers_done=len(rows),
            height_mm=round(len(rows) * self.prog.layer_mm, 4),
            times_s=self.times,
            layer_period_s=dict(mean=sum(periods) / len(periods), min=min(periods), max=max(periods)) if periods else None,
            scan_s=stat("scan_s"), recoat_s=stat("recoat_s"), dwell_s=stat("dwell_s"), hold_s=stat("hold_s"),
            energy_J=stat("energy_J"),
            warnings=sorted(self.warned),
            states=[s.value for s in dict.fromkeys(self.sm.visited())],
        )
        if w is not None:
            out["sim"] = dict(argon_used_L=round(w.argon_used_L, 1), laser_on_s=round(w.laser_on_s, 2),
                              final_o2_ppm=round(w.o2, 1), plate_max_C=max((r["plate_C"] for r in self.log.samples),
                                                                           default=None))
            self.log.markers = list(w.markers)
        return out
