"""SCANLAB RTC5 PCIe board through RTC5DLLx64.dll with ctypes (Windows; the RTC5's DLL is Windows-only).

Every function name, argument type and unit below is from the RTC5 manual, Rev. 1.9 e (SCANLAB), page numbers in
PROTOTYPES. A public copy: https://manualedistruzioni.it/scanlab/recording-equipment/rtc-5-pc-interface-board/user-manual/12dpa
The DLL, the firmware files (RTC5OUT.out, RTC5RBF.rbf, RTC5DAT.dat) and correXion come from SCANLAB's download portal.

Units the RTC5 uses (manual pages): coordinates in bits, 20-bit signed in the real field [-524288, 524287] (p. 307,
349), K = 2^20 / a0 bits/mm (p. 119), read from the correction table with get_table_para(table, 1) (p. 285); speeds in
bits/ms as doubles (p. 438, 448); scanner delays in 10 us (p. 475); laser delays in 0.5 us (p. 442); ANALOG OUT1 12-bit,
0 = 0 V, 4095 = 10 V (p. 557); signal recording every Period x 10 us, up to 2^19 values per channel with set_trigger4
(p. 497, 294).

The RTC5's head connector speaks SL2-100 only (p. 41-42). A head with an XY2-100 interface, as the 2003 hurrySCAN 25,
needs SCANLAB's XY2-100 converter between them, which adds 10 us of latency: both laser delays are raised by that much
(p. 42, 442).
"""
from __future__ import annotations

import ctypes as C
import math
import sys
from typing import Dict, Optional

import numpy as np

from ..config import Config
from ..scanprog import layer_time, polylines
from .interfaces import ScanCard

U, I, D, P = C.c_uint32, C.c_int32, C.c_double, C.c_char_p
PU = C.POINTER(C.c_uint32)
# name: (restype, argtypes, manual page)
PROTOTYPES = {
    "init_rtc5_dll": (U, [], 306),
    "free_rtc5_dll": (None, [], 259),
    "rtc5_count_cards": (U, [], 396),
    "select_rtc": (U, [U], 403),
    "load_program_file": (U, [P], 340),
    "load_correction_file": (U, [P, U, U], 328),
    "select_cor_table": (None, [U, U], 400),
    "config_list": (None, [U, U], 243),
    "set_laser_mode": (None, [U], 443),
    "set_laser_control": (None, [U], 440),
    "set_port_default": (None, [U, U], 469),
    "enable_laser": (None, [], 255),
    "disable_laser": (None, [], 255),
    "get_table_para": (D, [U, U], 285),
    "get_last_error": (U, [], 270),
    "reset_error": (None, [U], 393),
    "get_head_status": (U, [U], 266),
    "get_status": (None, [PU, PU], 281),
    "read_status": (U, [], 390),
    "set_start_list": (None, [U], 489),
    "set_end_of_list": (None, [], 420),
    "execute_list": (None, [U], 256),
    "stop_execution": (None, [], 523),
    "write_da_1": (None, [U], 557),
    "goto_xy": (None, [I, I], 296),
    "get_time": (D, [], 286),
    "measurement_status": (None, [PU, PU], 365),
    "get_waveform": (None, [U, U, C.c_void_p], 294),
    # list commands
    "set_scanner_delays": (None, [U, U, U], 475),
    "set_laser_delays": (None, [I, U], 442),
    "set_delay_mode": (None, [U, U, U, U, U], 415),
    "set_jump_speed": (None, [D], 438),
    "set_mark_speed": (None, [D], 448),
    "jump_abs": (None, [I, I], 307),
    "mark_abs": (None, [I, I], 349),
    "write_da_1_list": (None, [U], 557),
    "set_laser_pin_out_list": (None, [U], 444),
    "set_trigger4": (None, [U, U, U, U, U], 497),
    "save_and_restart_timer": (None, [], 397),
    "list_nop": (None, [], 322),
}

# set_laser_control bits (p. 440): LASERON active-high (bit 3 = 0); laser signals suppressed automatically when the
# head's PowerOK or TempOK drops on X or Y (bits 16, 17, 19, 20), and then a /STOP is generated (bit 28).
LASER_CONTROL = (1 << 16) | (1 << 17) | (1 << 19) | (1 << 20) | (1 << 28)
# set_trigger4 signal numbers (p. 493-494): LASERON, SampleX, SampleY, ANALOG OUT1 value
TRACE_SIGNALS = (0, 7, 8, 33)
FIELD_MAX = 524287


class Rtc5Error(RuntimeError):
    pass


def load_dll(path: str = "RTC5DLLx64.dll"):
    if not sys.platform.startswith("win"):
        raise OSError("the RTC5 DLL is Windows-only; use ftctl.hw.sim on other systems")
    dll = C.WinDLL(path)
    for name, (res, args, _page) in PROTOTYPES.items():
        fn = getattr(dll, name)
        fn.restype = res
        fn.argtypes = args
    return dll


class Rtc5Scan(ScanCard):
    def __init__(self, cfg: Config, timing: dict, dll=None, card: int = 1):
        self.cfg = cfg
        self.timing = timing
        self.d = dll
        self.card = card
        self.K = cfg.scan.K()
        self.list_no = 1

    # ------------------------------------------------------------------ conversions
    def bits(self, xy) -> tuple:
        sc = self.cfg.scan
        x, y = float(xy[0]) - sc.x_offset_mm, float(xy[1]) - sc.y_offset_mm
        if sc.swap_xy:
            x, y = y, x
        if sc.flip_x:
            x = -x
        if sc.flip_y:
            y = -y
        bx, by = int(round(x * self.K)), int(round(y * self.K))
        if abs(bx) > FIELD_MAX or abs(by) > FIELD_MAX:
            raise Rtc5Error(f"point {xy} mm is outside the RTC5 field (K = {self.K:.1f} bits/mm)")
        return bx, by

    def da(self, P_W: float) -> int:
        V = self.cfg.laser.analog_V(P_W)
        return int(min(max(round(V / 10.0 * 4095), 0), 4095))

    @staticmethod
    def ticks10(t_s: float) -> int:
        return int(math.ceil(t_s / 10e-6 - 1e-9))

    @staticmethod
    def half_us(t_s: float) -> int:
        return int(round(t_s / 0.5e-6))

    def _check(self, where: str):
        err = self.d.get_last_error()
        if err:
            raise Rtc5Error(f"{where}: get_last_error = {err:#x}")

    # ------------------------------------------------------------------ ScanCard
    def open(self) -> None:
        d, sc = self.d, self.cfg.scan
        if d is None:
            d = self.d = load_dll()
        err = d.init_rtc5_dll()
        if err:
            raise Rtc5Error(f"init_rtc5_dll = {err:#x}")
        if d.rtc5_count_cards() < self.card:
            raise Rtc5Error("no RTC5 board found")
        d.select_rtc(self.card)
        err = d.load_program_file(sc.rtc_dir.encode())
        if err:
            raise Rtc5Error(f"load_program_file = {err} (manual p. 340)")
        err = d.load_correction_file(sc.correction_file.encode(), 1, 2)
        if err:
            raise Rtc5Error(f"load_correction_file = {err} (manual p. 328)")
        d.select_cor_table(1, 0)
        d.config_list(2 ** 19, 2 ** 19)
        d.set_laser_mode(0)                  # CO2 mode: LASERON is the gate; LASER1/LASER2 are not connected
        d.set_laser_control(LASER_CONTROL)
        d.set_port_default(0, 0)             # ANALOG OUT1 -> 0 V whenever a list stops
        d.set_port_default(4, 0)             # DIGITAL OUT1/2 (layer marker) -> low whenever a list stops
        d.write_da_1(0)
        K = d.get_table_para(1, 1)
        if K and K > 0:
            self.K = K
        d.enable_laser()
        self._check("open")

    def load_layer(self, layer, laser_cfg=None) -> dict:
        d, tm, sc = self.d, self.timing, self.cfg.scan
        lat = sc.xy2_converter_latency_s
        d.set_start_list(self.list_no)
        d.set_laser_pin_out_list(1)                     # layer marker up: DIGITAL OUT1, LASER connector pin 12
        if sc.record_trace:
            d.set_trigger4(1, *TRACE_SIGNALS)           # every 10 us
        d.save_and_restart_timer()
        d.set_scanner_delays(self.ticks10(tm["jump_delay"]), self.ticks10(tm["mark_delay"]),
                             self.ticks10(tm["polygon_delay"]))
        d.set_laser_delays(self.half_us(tm["laser_on_delay"] + lat), self.half_us(tm["laser_off_delay"] + lat))
        d.set_delay_mode(0, 0, 2 ** 32 - 1, self.ticks10(tm["jump_delay_min"]), int(round(tm["jump_limit"] * self.K)))
        d.set_jump_speed(tm["v_jump"] * self.K / 1000.0)
        cur_P = cur_v = None
        n_mark = 0
        for start, run in polylines(layer):
            d.jump_abs(*self.bits(start))
            for p1, P_W, v, _kind in run:
                if P_W != cur_P:
                    d.write_da_1_list(self.da(P_W))
                    cur_P = P_W
                if v != cur_v:
                    d.set_mark_speed(v * self.K / 1000.0)
                    cur_v = v
                d.mark_abs(*self.bits(p1))
                n_mark += 1
        d.write_da_1_list(0)
        d.jump_abs(0, 0)
        d.list_nop()                                    # lets the last scanner delay finish before the timer stops
        d.save_and_restart_timer()
        d.set_laser_pin_out_list(0)                     # layer marker down
        d.set_end_of_list()
        self._check(f"load layer {layer.index}")
        lt = layer_time(layer, tm)
        lt["n_mark_list"] = n_mark
        return lt

    def start(self) -> None:
        self.d.execute_list(self.list_no)

    def busy(self) -> bool:
        s, p = C.c_uint32(0), C.c_uint32(0)
        self.d.get_status(C.byref(s), C.byref(p))
        return bool(s.value & 1)

    def stop(self) -> None:
        self.d.stop_execution()
        self.d.write_da_1(0)

    def head_status(self) -> Dict[str, bool]:
        s = self.d.get_head_status(1)                   # p. 266: bit 3/4 PosAck X/Y, bit 6 temp OK, bit 7 power OK
        return dict(pos_x=bool(s & 8), pos_y=bool(s & 16), temp=bool(s & 64), power=bool(s & 128))

    def last_error(self) -> int:
        return int(self.d.get_last_error())

    def list_time(self) -> Optional[float]:
        return float(self.d.get_time())

    def trace(self) -> Optional[dict]:
        busy, pos = C.c_uint32(0), C.c_uint32(0)
        self.d.measurement_status(C.byref(busy), C.byref(pos))
        if busy.value:
            return None
        n = int(pos.value) + 1
        out = {}
        for ch, name in zip((1, 2, 3, 4), ("laser_on", "x_bits", "y_bits", "da")):
            buf = np.zeros(n, dtype=np.int32)
            self.d.get_waveform(ch, n, buf.ctypes.data)
            out[name] = buf
        out["t_s"] = np.arange(n) * 10e-6
        out["x_mm"] = out["x_bits"] / self.K
        out["y_mm"] = out["y_bits"] / self.K
        return out

    def close(self) -> None:
        if self.d is not None:
            self.d.disable_laser()
            self.d.free_rtc5_dll()


class FakeRtc5Dll:
    """Stands in for RTC5DLLx64.dll in tests: records every call; a list 'runs' for a set number of get_status calls."""

    def __init__(self, K: float = 6000.0, busy_polls: int = 3):
        self.calls = []
        self.K = K
        self.busy_polls = busy_polls
        self._busy = 0
        self.head = 0xFD

    def __getattr__(self, name):
        if name not in PROTOTYPES:
            raise AttributeError(name)

        def f(*args):
            self.calls.append((name, args))
            if name == "get_table_para":
                return self.K
            if name == "get_head_status":
                return self.head
            if name == "rtc5_count_cards":
                return 1
            if name == "execute_list":
                self._busy = self.busy_polls
            if name == "get_status":
                args[0]._obj.value = 1 if self._busy > 0 else 0
                self._busy -= 1
                return None
            if name == "measurement_status":
                args[0]._obj.value = 0
                args[1]._obj.value = 9
                return None
            if name == "get_time":
                return 3.14
            return 0 if PROTOTYPES[name][0] is not None else None
        return f

    def names(self):
        return [c[0] for c in self.calls]
