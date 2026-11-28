"""Turn the build file (scan_program.py's NPZ) into SCANLAB RTC5 list commands, one list per layer (#260).

Function names, arguments and units are from SCANLAB's "RTC5 PC Interface Board, Installation and Operation" manual,
Rev. 1.9 e (2014-09-09); page numbers in brackets. Read through a public mirror; SCANLAB's own copy comes with the
RTC5 software. Not run against a card: this machine has none.

  init_rtc5_dll() [306], select_rtc(CardNo) [403], load_program_file(Path) [340],
  load_correction_file(Name, No, Dim) [328], select_cor_table(HeadA, HeadB) [400], reset_error(Code) [393],
  set_laser_mode(Mode) [443], set_laser_control(Ctrl) [440], config_list(Mem1, Mem2) [243],
  set_start_list(ListNo) [489], set_end_of_list() [420], execute_list(ListNo) [256], get_status(&Status, &Pos) [281],
  read_status() [390], get_head_status(Head) [266],
  set_jump_speed(Speed) [438], set_mark_speed(Speed) [448]          bits per ms (double), v = Speed / K
  set_laser_delays(LaserOnDelay, LaserOffDelay) [442]                 1 bit = 0.5 us
  set_scanner_delays(Jump, Mark, Polygon) [475]                       1 bit = 10 us
  set_delay_mode(...) [415]                                           variable jump and polygon delays (arguments
                                                                      not transcribed: check p. 415 before use)
  jump_abs(X, Y) [307], mark_abs(X, Y) [349]                          bits, clipped to +-524288 (20-bit field)
  write_da_1_list(Value) [557]                                        12 bit: 0 = 0 V, 4095 = 10 V (ANALOG OUT1)
  long_delay(Delay) [348]                                             1 bit = 10 us
  set_sky_writing_para(Timelag, LaserOnShift, Nprev, Npost) [481], set_sky_writing_mode(Mode) [479]
  List memory [69-70]: 2^20 entries; lists 1 and 2 hold 4000 commands each unless config_list changes them.
  Calibration [119]: K = 2^20 / a0 bits per mm for a correction table of image field a0 (correXion sets it).

The plate frame of the build file is turned into the lens frame by the recommended axis offset (optics.py AXIS: the
lens axis meets the bed 30 mm in front of the plate centre) and an axis map (which galvo is X; set it from the
first burned cross).

Run: python desktop-lpbf/fast-track/process/rtc5_list.py   (writes out/rtc5_layer1.txt and prints the per-layer counts)
"""
from __future__ import annotations

import ctypes
import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
import scan_program as SPG  # noqa: E402

BITS = 2 ** 20                     # RTC5 field, 20 bit signed (+-524288)
A0_MM = 157.0                      # example: correction table over the LINOS 157 x 157 mm field -> K = 6679 bits/mm
K_DEFAULT = BITS / A0_MM
AXIS = (0.0, -30.0)                # lens axis on the bed, plate frame (optics.py)
AXIS_MAP = ((1, 0), (0, 1))        # plate (x, y) -> head (X, Y); set from the first burned cross
P_FULL = 400.0                     # W at 10 V on the IPG analog input (YLR: 0-10 V for 0-100 %; check the unit)
PARK = AXIS                        # park the beam on the lens axis, off the plate, between layers


def to_bits(x, y, K=K_DEFAULT):
    u, v = x - AXIS[0], y - AXIS[1]
    X = AXIS_MAP[0][0] * u + AXIS_MAP[0][1] * v
    Y = AXIS_MAP[1][0] * u + AXIS_MAP[1][1] * v
    Xb, Yb = int(round(X * K)), int(round(Y * K))
    if max(abs(Xb), abs(Yb)) > 524287:
        raise ValueError(f"({x:.2f}, {y:.2f}) is outside the RTC5 field")
    return Xb, Yb


def da_value(P):
    return int(round(min(max(P / P_FULL, 0.0), 1.0) * 4095))


def layer_commands(segs, kinds, pidx, parts, psets, tm: SPG.Timing, list_no=1, K=K_DEFAULT):
    """The RTC5 command list of one layer: [(name, args), ...]."""
    c = [("set_start_list", (list_no,)),
         ("set_laser_delays", (int(round(tm.laser_on_delay / 0.5e-6)), int(round(tm.laser_off_delay / 0.5e-6)))),
         ("set_scanner_delays", (int(round(tm.jump_delay / 10e-6)), int(round(tm.mark_delay / 10e-6)),
                                 int(round(tm.polygon_delay / 10e-6)))),
         ("set_jump_speed", (tm.v_jump * K / 1000.0,))]
    pos = None
    cur = None
    for s, kd, ii in zip(segs, kinds, pidx):
        ps = psets[parts[ii].pset]
        P, v = (ps.P_hatch, ps.v_hatch) if kd == 0 else (ps.P_contour, ps.v_contour)
        if cur != (P, v):
            c.append(("set_mark_speed", (v * K / 1000.0,)))
            c.append(("write_da_1_list", (da_value(P),)))
            cur = (P, v)
        a = to_bits(s[0], s[1], K)
        b = to_bits(s[2], s[3], K)
        if pos is None or abs(a[0] - pos[0]) > 6 or abs(a[1] - pos[1]) > 6:     # > ~1 um: a jump
            c.append(("jump_abs", a))
        c.append(("mark_abs", b))
        pos = b
    c.append(("jump_abs", to_bits(*PARK, K)))
    c.append(("set_end_of_list", ()))
    return c


def dry_run_time(cmds, tm: SPG.Timing, K=K_DEFAULT):
    """List execution time from the commands, with the same delay rules as scan_program.layer_time (fixed jump
    delay here: set_delay_mode's variable jump delay is not used in this listing)."""
    t, pos, v_mark, v_jump, marking = 0.0, None, None, None, False
    jd = md = pd = 0.0
    for name, args in cmds:
        if name == "set_scanner_delays":
            jd, md, pd = (x * 10e-6 for x in args)
        elif name == "set_jump_speed":
            v_jump = args[0] / K * 1000.0
        elif name == "set_mark_speed":
            v_mark = args[0] / K * 1000.0
        elif name == "jump_abs":
            if marking:
                t += md
                marking = False
            L = 0.0 if pos is None else math.hypot(args[0] - pos[0], args[1] - pos[1]) / K
            t += math.ceil(L / v_jump / 10e-6) * 10e-6 + jd
            pos = args
        elif name == "mark_abs":
            if marking:
                t += pd
            L = math.hypot(args[0] - pos[0], args[1] - pos[1]) / K
            t += math.ceil(L / v_mark / 10e-6 - 1e-9) * 10e-6
            pos = args
            marking = True
    return t


class RTC5:
    """ctypes binding of the calls used here (Windows, RTC5DLLx64.dll from SCANLAB's RTC5 software). Signatures
    follow the manual's C prototypes: UINT arguments as c_uint, signed positions as c_int, speeds as c_double."""
    SIG = {
        "init_rtc5_dll": ([], ctypes.c_uint), "free_rtc5_dll": ([], None), "select_rtc": ([ctypes.c_uint], ctypes.c_uint),
        "load_program_file": ([ctypes.c_char_p], ctypes.c_uint),
        "load_correction_file": ([ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint], ctypes.c_uint),
        "select_cor_table": ([ctypes.c_uint, ctypes.c_uint], None), "reset_error": ([ctypes.c_uint], None),
        "set_laser_mode": ([ctypes.c_uint], ctypes.c_uint), "set_laser_control": ([ctypes.c_uint], None),
        "set_start_list": ([ctypes.c_uint], None), "set_end_of_list": ([], None), "execute_list": ([ctypes.c_uint], None),
        "read_status": ([], ctypes.c_uint), "get_head_status": ([ctypes.c_uint], ctypes.c_uint),
        "get_status": ([ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)], None),
        "set_jump_speed": ([ctypes.c_double], None), "set_mark_speed": ([ctypes.c_double], None),
        "set_laser_delays": ([ctypes.c_int, ctypes.c_uint], None),
        "set_scanner_delays": ([ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None),
        "jump_abs": ([ctypes.c_int, ctypes.c_int], None), "mark_abs": ([ctypes.c_int, ctypes.c_int], None),
        "write_da_1_list": ([ctypes.c_uint], None), "long_delay": ([ctypes.c_uint], None),
    }

    def __init__(self, dll_path="RTC5DLLx64.dll"):
        self.dll = ctypes.WinDLL(dll_path)          # only on the Windows PC with the card
        for name, (argt, rest) in self.SIG.items():
            f = getattr(self.dll, name)
            f.argtypes, f.restype = argt, rest

    def start(self, program_dir: str, cor_file: str):
        err = self.dll.init_rtc5_dll()
        if err:
            raise RuntimeError(f"init_rtc5_dll: {err}")
        self.dll.select_rtc(1)
        self.dll.reset_error(0xFFFFFFFF)
        if self.dll.load_program_file(program_dir.encode()):
            raise RuntimeError("load_program_file")
        if self.dll.load_correction_file(cor_file.encode(), 1, 2):
            raise RuntimeError("load_correction_file")
        self.dll.select_cor_table(1, 0)

    def run(self, cmds, list_no=1, timeout_s=60.0):
        """Load one layer's list, start it, wait until the board is no longer busy."""
        import time
        for name, args in cmds:
            getattr(self.dll, name)(*args)
        self.dll.execute_list(list_no)
        st, pos = ctypes.c_uint(), ctypes.c_uint()
        t0 = time.time()
        while True:
            self.dll.get_status(ctypes.byref(st), ctypes.byref(pos))
            if not (st.value & 1):                      # bit 0 BUSY
                return
            if time.time() - t0 > timeout_s:
                raise TimeoutError("list still busy")
            time.sleep(0.005)


def main():
    path = OUT / "build_first_coupons_15mm.npz"
    segs, kinds, pidx, ptr, meta = SPG.load_build(path)
    parts = [SPG.Part(**p) for p in meta["parts"]]
    psets = {k: SPG.ParamSet(**v) for k, v in meta["psets"].items()}
    tm = SPG.Timing(**meta["timing"])
    counts, worst = [], 0
    for k in range(len(ptr) - 1):
        a, b = ptr[k], ptr[k + 1]
        cmds = layer_commands(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm, list_no=1 + k % 2)
        counts.append(len(cmds))
        if k == 0:
            lines = [f"# RTC5 list for layer 1 of {path.name}: {len(cmds)} commands; K = {K_DEFAULT:.1f} bits/mm "
                     f"(2^20 / {A0_MM:g} mm, an example: use the K of the correXion table); lens axis at plate {AXIS}",
                     f"# dry-run list time {dry_run_time(cmds, tm):.3f} s (fixed jump delay); scan_program.layer_time "
                     f"{SPG.layer_time(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm)['t_list']:.3f} s (variable)"]
            lines += [f"{n}({', '.join(f'{x:.1f}' if isinstance(x, float) else str(x) for x in args)})" for n, args in cmds]
            (OUT / "rtc5_layer1.txt").write_text("\n".join(lines) + "\n")
            print(lines[0]); print(lines[1])
    print(f"{len(counts)} layers; commands per layer {min(counts)}-{max(counts)} (lists 1 and 2 hold 4000 each)")
    info = dict(K_bits_per_mm=K_DEFAULT, axis=AXIS, commands_min=min(counts), commands_max=max(counts),
                list_capacity=4000, mark_speed_bits_per_ms=1250.0 * K_DEFAULT / 1000.0,
                jump_speed_bits_per_ms=tm.v_jump * K_DEFAULT / 1000.0,
                laser_delays_bits=(int(round(tm.laser_on_delay / 0.5e-6)), int(round(tm.laser_off_delay / 0.5e-6))),
                scanner_delays_bits=(int(round(tm.jump_delay / 10e-6)), int(round(tm.mark_delay / 10e-6)),
                                     int(round(tm.polygon_delay / 10e-6))),
                da_255W=da_value(255.0), da_150W=da_value(150.0))
    # the one-layer commissioning programs (rungs 1-3)
    info["ladder"] = {}
    for name in ("rung1_bare_plate", "rung2_single_tracks"):
        p = OUT / f"{name}.npz"
        if not p.exists():
            continue
        s2, k2, i2, ptr2, m2 = SPG.load_build(p)
        parts2 = [SPG.Part(**q) for q in m2["parts"]]
        psets2 = {kk: SPG.ParamSet(**v) for kk, v in m2["psets"].items()}
        cmds = layer_commands(s2, k2, i2, parts2, psets2, tm)
        txt = [f"# RTC5 list for {p.name}: {len(cmds)} commands, dry-run {dry_run_time(cmds, tm):.3f} s; "
               f"K = {K_DEFAULT:.1f} bits/mm (example); lens axis at plate {AXIS}"]
        txt += [f"{n}({', '.join(f'{x:.1f}' if isinstance(x, float) else str(x) for x in args)})" for n, args in cmds]
        (OUT / f"rtc5_{name}.txt").write_text("\n".join(txt) + "\n")
        info["ladder"][name] = dict(commands=len(cmds), dry_run_s=dry_run_time(cmds, tm))
    (OUT / "rtc5.json").write_text(json.dumps(info, indent=1))
    print(info)


if __name__ == "__main__":
    main()
