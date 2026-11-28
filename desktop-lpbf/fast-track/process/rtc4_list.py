"""Turn the build file (scan_program.py's NPZ) into SCANLAB RTC4 list commands, one list per layer (round 3, #260).

Round 2 replaced the RTC5 with a used RTC4 PCIe, because the RTC5's head connector speaks SL2-100 and the 2003
hurrySCAN 25 takes XY2-100 (control/README.md §6). rtc5_list.py's lists are RTC5 lists; this is the same program for
the RTC4. The command names and their order follow the supervisor's RTC4 backend, control/ftctl/hw/rtc4.py
(Rtc4Scan.load_layer), so a list written here is the list the supervisor loads. Not run against a card: there is none.

RTC4 units (RTC4 manual Rev. 1.3 e, and the RTC5 manual Rev. 1.9 e §2.7 "Notes for RTC4 users", pp. 31-34, as cited
in rtc4.py; see the README for what was and wasn't confirmed):
  jump_abs(X, Y), mark_abs(X, Y)            16-bit signed field, -32768 ... 32767 bits (RTC5: 20-bit)
  K16 = K20 / 16 bits per mm                here from ftctl's Scan.K(): 2^20 / (2 f theta) / 16, f = 254 mm,
                                            theta = 0.35 rad (hurrySCAN typical angle): 368.6 bits/mm, 2.71 um a bit;
                                            the real K is the .ctb correction table's
  set_mark_speed / set_jump_speed(v)        bits per ms (double): v [mm/s] x K / 1000
  set_laser_delays(on, off)                 1 us a bit, signed 16-bit (RTC5: 0.5 us); rtc4.py keeps off > on
  set_scanner_delays(jump, mark, polygon)   10 us a bit
  set_delay_mode(VarPoly, DirectMove3D, EdgeLevel, MinJumpDelay, JumpLengthLimit)
                                            as rtc4.py: (0, 0, 65500 = off, min jump delay in 10 us, limit in bits)
  write_da_1_list(V)                        10-bit, 0 ... 1023 = 0 ... 10 V with ANALOG OUT1 jumpered to 0-10 V
                                            (RTC5: 12-bit); the IPG takes 1-10 V for 10-100 % (ftctl config.Laser)
  write_io_port_list(bits)                  16-bit digital out (EXTENSION 1); bit 0 = the layer marker (rtc4.py)
  list_nop(), set_start_list(n), set_end_of_list(), execute_list(n)
  list memory                               two lists of 4,000 commands (rtc4.py: LIST_MAX)
  list clock                                10 us (vectors are stepped every 10 us, as on the RTC5)

The plate frame of the build file (cad/ft_model.py: origin at the plate centre) is turned into the head frame by the
lens-axis offset (CAD v2 P['axis_off'] = (0, -30): the lens axis meets the bed 30 mm in front of the plate centre) and
an axis map (set from the first burned cross). Between layers the beam parks on the lens axis, (0, 0) bits, off the
plate, as rtc4.py does.

Run: python desktop-lpbf/fast-track/process/rtc4_list.py   (writes out/rtc4_*.txt and out/rtc4.json; ~10 s)
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
import scan_program as SPG  # noqa: E402

FIELD_MAX4 = 32767                 # rtc4.py
LIST_MAX = 4000                    # rtc4.py: commands per list (lists 1 and 2)
F_MM, THETA = 254.0, 0.35          # control/ftctl/config.py Scan: focal_mm, field_angle_rad
K20 = 2 ** 20 / (2.0 * F_MM * THETA)
K16 = K20 / 16.0                   # 368.6 bits/mm (rtc4.py: Rtc4Scan.K = cfg.scan.K() / 16)
K16_LINOS = 2 ** 16 / 157.0        # 417.4 bits/mm if the table spans the LINOS 157 mm field (rtc5_list.py's example)
AXIS = (0.0, -30.0)                # CAD v2 P['axis_off'] (checked against ft_model in main() when CadQuery imports)
AXIS_MAP = ((1, 0), (0, 1))        # plate (x, y) -> head (X, Y); set from the first burned cross
P_FULL = 400.0                     # W at 10 V
V_MIN, V_MAX = 1.0, 10.0           # IPG YLR analog input: 1-10 V = 10-100 % (ftctl config.Laser)
DA_BITS = 1023
PARK = (0, 0)                      # bits: the lens axis


def to_bits(x, y, K=K16):
    u, v = x - AXIS[0], y - AXIS[1]
    X = AXIS_MAP[0][0] * u + AXIS_MAP[0][1] * v
    Y = AXIS_MAP[1][0] * u + AXIS_MAP[1][1] * v
    Xb, Yb = int(round(X * K)), int(round(Y * K))
    if max(abs(Xb), abs(Yb)) > FIELD_MAX4:
        raise ValueError(f"({x:.2f}, {y:.2f}) mm is outside the RTC4's 16-bit field at K = {K:.1f} bits/mm")
    return Xb, Yb


def da4(P):
    """10-bit ANALOG OUT1 value for P watts: 0 V below the laser's 10 % (40 W) setpoint, else V = 10 P / 400."""
    if P <= 0:
        return 0
    V = min(max(V_MAX * P / P_FULL, V_MIN), V_MAX)
    return int(round(V / 10.0 * DA_BITS))


def ticks10(t):
    return int(math.ceil(t / 10e-6 - 1e-9))


def layer_commands(segs, kinds, pidx, parts, psets, tm: SPG.Timing, list_no=1, K=K16):
    """The RTC4 command list of one layer, in rtc4.py's order: [(name, args), ...]."""
    on = int(round(tm.laser_on_delay / 1e-6))
    off = max(int(round(tm.laser_off_delay / 1e-6)), on + 1)
    c = [("set_start_list", (list_no,)),
         ("write_io_port_list", (1,)),
         ("set_scanner_delays", (ticks10(tm.jump_delay), ticks10(tm.mark_delay), ticks10(tm.polygon_delay))),
         ("set_laser_delays", (on, off)),
         ("set_delay_mode", (0, 0, 65500, ticks10(tm.jump_delay_min), min(int(round(tm.jump_limit * K)), 32500))),
         ("set_jump_speed", (tm.v_jump * K / 1000.0,))]
    pos = None
    cur_P = cur_v = None
    for s, kd, ii in zip(segs, kinds, pidx):
        ps = psets[parts[ii].pset]
        P, v = (ps.P_hatch, ps.v_hatch) if kd == 0 else (ps.P_contour, ps.v_contour)
        a = to_bits(s[0], s[1], K)
        b = to_bits(s[2], s[3], K)
        if pos is None or abs(a[0] - pos[0]) > 0 or abs(a[1] - pos[1]) > 0:
            c.append(("jump_abs", a))
        if P != cur_P:
            c.append(("write_da_1_list", (da4(P),)))
            cur_P = P
        if v != cur_v:
            c.append(("set_mark_speed", (v * K / 1000.0,)))
            cur_v = v
        c.append(("mark_abs", b))
        pos = b
    c += [("write_da_1_list", (0,)), ("jump_abs", PARK), ("list_nop", ()), ("write_io_port_list", (0,)),
          ("set_end_of_list", ())]
    return c


def dry_run(cmds, tm: SPG.Timing):
    """List time from the commands with the RTC4's rules as modelled here: 10 us clock, mark/jump durations rounded
    up to whole ticks, mark delay before a jump, polygon delay inside a polyline, and the variable jump delay of
    set_delay_mode (linear from MinJumpDelay at 0 to the full jump delay at JumpLengthLimit, as scan_program.py's
    layer_time assumes; the RTC4's exact rule is not confirmed). Also the laser-on time and the energy."""
    t, pos, v_mark, v_jump, marking = 0.0, (0, 0), None, None, False
    jd = md = pd = 0.0
    jmin, jlim = 0.0, 1
    on_d = off_d = 0.0
    P = 0.0
    seq, t_on, E = 0.0, 0.0, 0.0

    def close():
        nonlocal seq, t_on, E
        if seq > 0:
            on = max(seq - on_d + off_d, 0.0)
            t_on += on
            E += P * on
        seq = 0.0

    for name, args in cmds:
        if name == "set_scanner_delays":
            jd, md, pd = (x * 10e-6 for x in args)
        elif name == "set_laser_delays":
            on_d, off_d = args[0] * 1e-6, args[1] * 1e-6
        elif name == "set_delay_mode":
            jmin, jlim = args[3] * 10e-6, args[4]
        elif name == "set_jump_speed":
            v_jump = args[0]                                # bits/ms
        elif name == "set_mark_speed":
            v_mark = args[0]
        elif name == "write_da_1_list":
            close()                                         # a power change ends the polyline's laser sequence
            P = args[0] / DA_BITS * 10.0 / V_MAX * P_FULL
        elif name == "jump_abs":
            if marking:
                t += md
                close()
                marking = False
            L = math.hypot(args[0] - pos[0], args[1] - pos[1])
            if L > 0:
                d_ = jd if L >= jlim else jmin + (jd - jmin) * L / jlim
                t += math.ceil(L / v_jump / 1e-2 - 1e-9) * 10e-6 + math.ceil(d_ / 10e-6 - 1e-9) * 10e-6
            pos = args
        elif name == "mark_abs":
            if marking:
                t += pd
            L = math.hypot(args[0] - pos[0], args[1] - pos[1])
            dt = math.ceil(L / v_mark / 1e-2 - 1e-9) * 10e-6
            t += dt
            seq += dt
            pos = args
            marking = True
    return dict(t_list=t + tm.list_overhead, t_laser_on=t_on, energy_J=E)


def quantisation(segs, kinds, pidx, parts, psets, K):
    """What the 16-bit field does to layer 1: the largest rounding error of an end point, and the spread of the
    perpendicular spacing between neighbouring hatch lines after rounding, against the programmed hatch."""
    err = []
    for s in segs:
        for x, y in ((s[0], s[1]), (s[2], s[3])):
            Xb, Yb = to_bits(x, y, K)
            err.append(math.hypot(Xb / K - (x - AXIS[0]), Yb / K - (y - AXIS[1])))
    dev = []
    for i in range(1, len(segs)):
        if kinds[i] or kinds[i - 1] or pidx[i] != pidx[i - 1]:
            continue
        h = psets[parts[pidx[i]].pset].hatch
        a0, a1 = np.array(to_bits(*segs[i - 1][:2], K), float) / K, np.array(to_bits(*segs[i - 1][2:], K), float) / K
        b0 = np.array(to_bits(*segs[i][:2], K), float) / K
        d = a1 - a0
        n_ = np.array([-d[1], d[0]]) / np.hypot(*d)
        gap = abs(float(np.dot(b0 - a0, n_)))
        g0 = abs(float(np.dot(np.array(segs[i][:2]) - np.array(segs[i - 1][:2]), n_)))
        if abs(g0 - h) < 0.02:                             # neighbouring lines of one meander only
            dev.append(gap - h)
    dev = np.array(dev) * 1000.0
    return dict(K_bits_per_mm=K, um_per_bit=1000.0 / K, endpoint_error_max_um=1000.0 * max(err),
                hatch_spacing_dev_um=dict(rms=float(np.sqrt(np.mean(dev ** 2))), max=float(np.abs(dev).max()),
                                          n=int(len(dev))))


def write_list(path, header, cmds):
    lines = header + [f"{n}({', '.join(f'{x:.3f}' if isinstance(x, float) else str(x) for x in args)})"
                      for n, args in cmds]
    path.write_text("\n".join(lines) + "\n")


def main():
    path = OUT / "build_first_coupons_15mm.npz"
    segs, kinds, pidx, ptr, meta = SPG.load_build(path)
    parts = [SPG.Part(**p) for p in meta["parts"]]
    psets = {k: SPG.ParamSet(**v) for k, v in meta["psets"].items()}
    tm = SPG.Timing(**meta["timing"])
    counts, times = [], []
    worst = (0, -1)
    info = dict(card="SCANLAB RTC4 PCIe (control/README.md §6)", backend="control/ftctl/hw/rtc4.py",
                K16_bits_per_mm=K16, K16_LINOS_bits_per_mm=K16_LINOS, K20_bits_per_mm=K20, axis=AXIS, park_bits=PARK,
                list_capacity=LIST_MAX, field_max_bits=FIELD_MAX4)
    for k in range(len(ptr) - 1):
        a, b = ptr[k], ptr[k + 1]
        cmds = layer_commands(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm, list_no=1 + k % 2)
        counts.append(len(cmds))
        if len(cmds) > worst[0]:
            worst = (len(cmds), k + 1)
        if k < 3 or k % 50 == 0:
            times.append((k + 1, dry_run(cmds, tm)["t_list"],
                          SPG.layer_time(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm)["t_list"]))
        if k == 0:
            dr = dry_run(cmds, tm)
            lt = SPG.layer_time(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm)
            q = quantisation(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, K16)
            q2 = quantisation(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, K16_LINOS)
            xs = [abs(x) for n, args in cmds if n in ("jump_abs", "mark_abs") for x in args]
            header = [f"# RTC4 list for layer 1 of {path.name}: {len(cmds)} commands (of {LIST_MAX} a list); "
                      f"K = {K16:.1f} bits/mm (16-bit; the .ctb table's K replaces it); lens axis at plate {AXIS}",
                      f"# dry run {dr['t_list']:.3f} s, laser on {dr['t_laser_on']:.3f} s, {dr['energy_J']:.0f} J; "
                      f"scan_program.layer_time {lt['t_list']:.3f} s, {lt['energy_J']:.0f} J; largest |coordinate| "
                      f"{max(xs)} bits of {FIELD_MAX4}",
                      "# units: positions in bits; speeds bits/ms; laser delays 1 us; scanner delays 10 us; "
                      "write_da_1_list 10-bit (1023 = 10 V = 400 W)"]
            write_list(OUT / "rtc4_layer1.txt", header, cmds)
            info["layer1"] = dict(commands=len(cmds), dry_run_s=dr["t_list"], laser_on_s=dr["t_laser_on"],
                                  energy_J=dr["energy_J"], layer_time_s=lt["t_list"], layer_energy_J=lt["energy_J"],
                                  max_abs_bits=max(xs), quantisation=q, quantisation_K_LINOS=q2)
            print(header[0]); print(header[1])
    info.update(commands_min=min(counts), commands_max=max(counts), worst_layer=worst[1],
                layers=len(counts), layers_over_list=int(sum(c > LIST_MAX for c in counts)),
                dry_run_vs_layer_time=[dict(layer=l_, dry_run_s=round(d_, 4), layer_time_s=round(t_, 4))
                                       for l_, d_, t_ in times],
                mark_speed_bits_per_ms={"1250 mm/s": 1250.0 * K16 / 1000.0, "800 mm/s": 800.0 * K16 / 1000.0},
                jump_speed_bits_per_ms=tm.v_jump * K16 / 1000.0,
                laser_delays_us=(int(round(tm.laser_on_delay / 1e-6)), int(round(tm.laser_off_delay / 1e-6))),
                scanner_delays_10us=(ticks10(tm.jump_delay), ticks10(tm.mark_delay), ticks10(tm.polygon_delay)),
                delay_mode=(0, 0, 65500, ticks10(tm.jump_delay_min), int(round(tm.jump_limit * K16))),
                da={f"{P:g} W": da4(P) for P in (50.0, 150.0, 255.0, 400.0)},
                da_step_W=P_FULL / DA_BITS, da_step_W_rtc5=P_FULL / 4095)
    print(f"{len(counts)} layers; commands per layer {min(counts)}-{max(counts)} (layer {worst[1]}); "
          f"lists hold {LIST_MAX}")
    # the one-layer commissioning programs (rungs 1-3; rung 3 is rung 2's file at 200 C)
    info["ladder"] = {}
    for name in ("rung1_bare_plate", "rung2_single_tracks"):
        p = OUT / f"{name}.npz"
        s2, k2, i2, ptr2, m2 = SPG.load_build(p)
        parts2 = [SPG.Part(**q) for q in m2["parts"]]
        psets2 = {kk: SPG.ParamSet(**v) for kk, v in m2["psets"].items()}
        cmds = layer_commands(s2, k2, i2, parts2, psets2, tm)
        dr = dry_run(cmds, tm)
        lt = SPG.layer_time(s2, k2, i2, parts2, psets2, tm)
        xs = [abs(x) for n, args in cmds if n in ("jump_abs", "mark_abs") for x in args]
        note = " (also rung 3: the same list on the plate at 200 C)" if name.startswith("rung2") else ""
        header = [f"# RTC4 list for {p.name}{note}: {len(cmds)} commands, dry run {dr['t_list']:.3f} s, "
                  f"laser on {dr['t_laser_on']:.3f} s, {dr['energy_J']:.1f} J (layer_time {lt['t_list']:.3f} s); "
                  f"K = {K16:.1f} bits/mm; lens axis at plate {AXIS}",
                  "# units: positions in bits; speeds bits/ms; laser delays 1 us; scanner delays 10 us; "
                  "write_da_1_list 10-bit (1023 = 10 V = 400 W)"]
        write_list(OUT / f"rtc4_{name}.txt", header, cmds)
        info["ladder"][name] = dict(commands=len(cmds), dry_run_s=dr["t_list"], laser_on_s=dr["t_laser_on"],
                                    energy_J=dr["energy_J"], layer_time_s=lt["t_list"], max_abs_bits=max(xs),
                                    powers_da={f"{q.P_hatch:g} W": da4(q.P_hatch) for q in psets2.values()})
        print(header[0])
    (OUT / "rtc4.json").write_text(json.dumps(info, indent=1))
    return info


if __name__ == "__main__":
    main()
