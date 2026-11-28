"""SCANLAB RTC4 (PCI/PCIe) through its DLL with ctypes: the same ScanCard as rtc5.Rtc5Scan with the RTC4's differences.

Why: the hurrySCAN 25 (2003) has an XY2-100 interface. The RTC4's 25-pin D-sub scan head connector speaks XY2-100
directly (RTC4 manual Rev. 1.3 e, p. 54: CLOCK 1/14, SYNC 2/15, CHAN1 3/16, CHAN2 4/17, CHAN3 5/18, STATUS 6/19, the
same pins as the head's DIGITAL IN); the RTC5 needs SCANLAB's XY2-100 converter (RTC5 manual Rev. 1.9 e, pp. 41-43).
RTC4 manual: https://www.manualslib.com/manual/1581336/Scanlab-Rtc-4.html

Differences used here (RTC5 manual Rev. 1.9 e, 2.7 "Notes for RTC4 users", pp. 31-34, unless marked):
- no init_rtc5_dll; boards counted with rtc4_count_cards; load_program_file takes the DSP program file (RTC4D2.hex for
  2D, RTC4 manual p. 89) and load_correction_file takes a .ctb file and its own scale/rotation/offset arguments;
  SCANLAB recommends loading the correction file before the program file (RTC4 manual p. 63);
- no set_laser_control (so no automatic laser suppression on a head status error: the supervisor's head check does it);
- coordinates 16-bit signed (-32768 ... 32767), K16 = K20 / 16 (p. 33; RTC4 manual pp. 89, 121);
- analog outputs 10-bit, 0-1023 (p. 33; RTC4 manual p. 123); ANALOG OUT1 must be jumpered to 0-10 V, not 0-2.56 V
  (RTC4 manual p. 59, 130);
- laser delays in 1 us, signed 16-bit (p. 33; RTC4 manual p. 107); scanner delays in 10 us; set_delay_mode with
  16-bit arguments, edgelevel 65500 = off (RTC4 manual p. 104);
- two lists of up to 4,000 commands (RTC4 manual pp. 104, 130); one FT-1 layer is ~1,100 commands;
- 9-pin laser connector (RTC5 manual p. 48, the laser adapter that copies it): 1 LASER1, 2 LASERON, 3 LASER2,
  4 ANALOG OUT1, 5 GND, 6-7 GND2, 8 /START, 9 /STOP. No BUSY OUT or 2-bit digital output: the layer marker goes
  on the 16-bit digital output port (EXTENSION 1, write_io_port_list, bit 0; RTC4 manual p. 123).
Checked in round 3 (2026-11-28) against SCANLAB's own RTC4expl.h and RTC4expl.cpp (explicit-linking header and
loader, (c) SCANLAB AG, v1.0 of 24 Jul 2013), as published in the public repo always-walking/rtctestcase
(src/include/; its bin/ also carries RTC4DLL.dll, RTC4DLLx64.dll and the RTC4D2/RTC4D3 program files):
- the 64-bit DLL is RTC4DLLx64.DLL: RTC4open() loads it `#if defined(_WIN64) || defined(WIN64)`, RTC4DLL.DLL otherwise;
- load_correction_file(const char* filename, short cortable, double kx, double ky, double phi, double xoffset,
  double yoffset) returns short; load_program_file(const char* name) returns short;
- enable_laser(void) and disable_laser(void) exist on the RTC4;
- select_rtc(unsigned short cardno) returns void on the RTC4 (the RTC5's returns the card number);
- every other prototype below matches the header. SpiralLab's Sirius2 SDK (Windows x64 only) lists
  "SCANLAB RTC4 2023.11.02" from SCANLAB's download page as a dependency, so the package is still distributed.
"""
from __future__ import annotations

import ctypes as C
import sys

from ..config import Config
from ..scanprog import layer_time, polylines
from .rtc5 import Rtc5Error, Rtc5Scan

US, S16, D, P = C.c_ushort, C.c_short, C.c_double, C.c_char_p
PUS = C.POINTER(C.c_ushort)
PROTOTYPES4 = {
    "rtc4_count_cards": (US, []),
    "select_rtc": (None, [US]),                                # void on the RTC4 (RTC4expl.h)
    "load_correction_file": (S16, [P, S16, D, D, D, D, D]),    # (file, cortable, kx, ky, phi, xoffset, yoffset): RTC4expl.h
    "load_program_file": (S16, [P]),
    "select_cor_table": (None, [US, US]),
    "set_laser_mode": (None, [US]),
    "enable_laser": (None, []),                                # in RTC4expl.h
    "disable_laser": (None, []),
    "set_delay_mode": (None, [US, US, US, US, US]),
    "get_head_status": (US, [US]),
    "get_status": (None, [PUS, PUS]),
    "read_status": (US, []),
    "set_start_list": (None, [US]),
    "set_end_of_list": (None, []),
    "execute_list": (None, [US]),
    "stop_execution": (None, []),
    "write_da_1": (None, [US]),
    "write_io_port": (None, [US]),
    "set_scanner_delays": (None, [US, US, US]),
    "set_laser_delays": (None, [S16, S16]),
    "set_jump_speed": (None, [D]),
    "set_mark_speed": (None, [D]),
    "jump_abs": (None, [S16, S16]),
    "mark_abs": (None, [S16, S16]),
    "write_da_1_list": (None, [US]),
    "write_io_port_list": (None, [US]),
    "list_nop": (None, []),
}
FIELD_MAX4 = 32767
LIST_MAX = 4000


def load_dll4(path: str = "RTC4DLLx64.dll"):
    if not sys.platform.startswith("win"):
        raise OSError("the RTC4 DLL is Windows-only; use ftctl.hw.sim on other systems")
    dll = C.WinDLL(path)
    for name, (res, args) in PROTOTYPES4.items():
        fn = getattr(dll, name)
        fn.restype = res
        fn.argtypes = args
    return dll


class Rtc4Scan(Rtc5Scan):
    def __init__(self, cfg: Config, timing: dict, dll=None, card: int = 1,
                 program_file: str = r"C:\RTC4\RTC4D2.hex", correction_file: str = r"C:\RTC4\ft1_hs25_f254.ctb"):
        super().__init__(cfg, timing, dll, card)
        self.K = cfg.scan.K() / 16.0
        self.program_file = program_file
        self.correction_file = correction_file

    def bits(self, xy) -> tuple:
        bx, by = self._xy(xy)
        bx, by = int(round(bx * self.K)), int(round(by * self.K))
        if abs(bx) > FIELD_MAX4 or abs(by) > FIELD_MAX4:
            raise Rtc5Error(f"point {xy} mm is outside the RTC4 field (K = {self.K:.1f} bits/mm)")
        return bx, by

    def da(self, P_W: float) -> int:
        V = self.cfg.laser.analog_V(P_W)
        return int(min(max(round(V / 10.0 * 1023), 0), 1023))

    def open(self) -> None:
        d = self.d
        if d is None:
            d = self.d = load_dll4()
        if d.rtc4_count_cards() < self.card:
            raise Rtc5Error("no RTC4 board found")
        d.select_rtc(self.card)
        err = d.load_correction_file(self.correction_file.encode(), 1, 1.0, 1.0, 0.0, 0.0, 0.0)
        if err:
            raise Rtc5Error(f"RTC4 load_correction_file = {err}")
        err = d.load_program_file(self.program_file.encode())
        if err:
            raise Rtc5Error(f"RTC4 load_program_file = {err}")
        d.select_cor_table(1, 0)
        d.set_laser_mode(0)
        d.write_da_1(0)
        d.write_io_port(0)
        d.enable_laser()

    def _check(self, where: str):
        pass                                    # the RTC4 has no get_last_error; errors come back as return codes

    def load_layer(self, layer, laser_cfg=None) -> dict:
        d, tm = self.d, self.timing
        lat = 0.0                               # no converter on the RTC4
        n_cmd = 12 + 2 * len(layer) + 2 * sum(1 for _ in polylines(layer))
        if n_cmd > LIST_MAX - 10:
            raise Rtc5Error(f"layer {layer.index} needs ~{n_cmd} list commands; RTC4 lists hold {LIST_MAX} "
                            "(split the layer across both lists: not implemented)")
        d.set_start_list(self.list_no)
        d.write_io_port_list(1)                                  # layer marker: EXTENSION 1 DIGITAL_OUT0
        d.set_scanner_delays(self.ticks10(tm["jump_delay"]), self.ticks10(tm["mark_delay"]),
                             self.ticks10(tm["polygon_delay"]))
        on = int(round((tm["laser_on_delay"] + lat) / 1e-6))
        off = max(int(round((tm["laser_off_delay"] + lat) / 1e-6)), on + 1)   # the RTC4 wants off > on
        d.set_laser_delays(on, off)
        d.set_delay_mode(0, 0, 65500, self.ticks10(tm["jump_delay_min"]), min(int(round(tm["jump_limit"] * self.K)), 32500))
        d.set_jump_speed(min(tm["v_jump"] * self.K / 1000.0, 50000.0))
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
        d.list_nop()
        d.write_io_port_list(0)
        d.set_end_of_list()
        lt = layer_time(layer, tm)
        lt["n_mark_list"] = n_mark
        lt["n_commands"] = n_cmd
        return lt

    def busy(self) -> bool:
        b, p = C.c_ushort(0), C.c_ushort(0)
        self.d.get_status(C.byref(b), C.byref(p))
        return bool(b.value & 1)

    def stop(self) -> None:
        self.d.stop_execution()
        self.d.write_da_1(0)
        self.d.write_io_port(0)

    def last_error(self) -> int:
        return 0

    def list_time(self):
        return None

    def trace(self):
        return None

    def close(self) -> None:
        if self.d is not None:
            self.d.disable_laser()


class FakeRtc4Dll:
    def __init__(self, busy_polls: int = 2):
        self.calls = []
        self.busy_polls = busy_polls
        self._busy = 0
        self.head = 0xFD

    def __getattr__(self, name):
        if name not in PROTOTYPES4:
            raise AttributeError(f"{name} is not an RTC4 function used here")

        def f(*args):
            self.calls.append((name, args))
            if name == "rtc4_count_cards":
                return 1
            if name == "get_head_status":
                return self.head
            if name == "execute_list":
                self._busy = self.busy_polls
            if name == "get_status":
                args[0]._obj.value = 1 if self._busy > 0 else 0
                self._busy -= 1
                return None
            return 0 if PROTOTYPES4[name][0] is not None else None
        return f

    def names(self):
        return [c[0] for c in self.calls]
