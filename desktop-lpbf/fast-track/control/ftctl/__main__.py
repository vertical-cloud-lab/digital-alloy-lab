"""Command line.

  python -m ftctl simulate --layers 20                 # simulated build of the first 20 layers of the scan program
  python -m ftctl simulate --height 2 --no-vent        # a 2 mm build, left hot under argon at the end
  python -m ftctl simulate --layers 20 --fault o2_leak@layer5
  python -m ftctl info                                 # the scan program's layers and planned list times
  python -m ftctl interlock                            # exhaustive check of the hard-wired safety chain model

Run from desktop-lpbf/fast-track/control (or put that folder on PYTHONPATH).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

from .clock import SimClock
from .config import Config
from .hw.sim import make_sim_machine
from .logger import BuildLog
from .scanprog import find_program, layer_time, load_npz, synthetic
from .supervisor import Supervisor

FAULTS = {
    # name: (description, function(world))
    "o2_leak": ("lid gasket leak of 0.5 L/min of air", lambda w: setattr(w, "extra_leak_Lpm", 0.5)),
    "lid_open": ("lid opened (both lid-switch channels)", lambda w: setattr(w, "lid_closed", False)),
    "estop": ("E-stop pressed", lambda w: setattr(w, "estop_ok", False)),
    "stage_stall": ("piston stalls on its next move (Zaber FS)", lambda w: setattr(w.axes["piston"], "stall_next", True)),
    "tc_open": ("plate thermocouple open", lambda w: w.tc_open.add("plate")),
    "ssr_short": ("plate SSR fails shorted (heaters full on)", lambda w: w.heater_stuck_on.add("plate")),
    "back_reflection": ("laser reports high back reflection (STA bit 3)", lambda w: setattr(w, "laser_bits", 1 << 3)),
    "cover_slide": ("cover slide fouled: 8 % of the beam absorbed at the window", lambda w: setattr(w, "cover_slide_fouling", 0.08)),
    "room_o2": ("room O2 falls to 19.0 %", lambda w: setattr(w, "room_o2_pct", 19.0)),
}


def load_program(arg):
    if arg == "synthetic":
        return synthetic(30)
    p = find_program(arg)
    if p is None:
        print("no scan program found; using a synthetic 10 x 10 mm square", file=sys.stderr)
        return synthetic(100)
    return load_npz(p)


def cmd_simulate(a):
    cfg = Config()
    if a.no_vent:
        cfg.vent_after_build = False
    prog = load_program(a.program)
    n = prog.n_layers
    if a.height:
        a.layers = int(round(a.height / prog.layer_mm))
    layers = list(range(min(a.layers or n, n)))
    clock = SimClock(speed=a.speed)
    m = make_sim_machine(cfg, clock, prog.timing(), seed=a.seed)
    out = pathlib.Path(a.out)
    log = BuildLog(out, clock, a.name)
    sup = Supervisor(m, cfg, prog, log, clock)
    for spec in a.fault or []:
        name, _, when = spec.partition("@")
        desc, fn = FAULTS[name]
        if when.startswith("layer"):
            m.world.on_layer(int(when[5:]), fn)
        else:
            m.world.at(float(when or 0), fn)
        print(f"fault scheduled: {desc} at {when}")
    wall = time.time()
    summ = sup.run(layers, startup=not a.no_startup, finish=not a.no_finish)
    wall = time.time() - wall
    summ["wall_clock_s"] = round(wall, 2)
    print(json.dumps(summ, indent=1, default=str))
    return 0 if summ["result"] == "complete" else 2


def cmd_info(a):
    prog = load_program(a.program)
    tm = prog.timing()
    print(f"{prog.source}: {prog.n_layers} layers of {prog.layer_mm * 1000:.0f} um, {len(prog.segs)} vectors")
    tot = 0.0
    for k in list(range(min(prog.n_layers, a.layers))):
        lt = layer_time(prog.layer(k), tm)
        tot += lt["t_list"]
        print(f"layer {k:4d}: {lt['n_mark']:4d} marks, {lt['n_jump']:4d} jumps, list {lt['t_list']:.3f} s, laser on "
              f"{lt['t_laser_on']:.3f} s, {lt['energy_J']:.0f} J")
    print(f"total list time of the first {a.layers} layers: {tot:.1f} s")


def cmd_study_dwell(a):
    from .studies import dwell_study, dwell_at_conductance
    prog = load_program(a.program)
    if a.g_pb is not None:
        out = a.out.replace("dwell-study.csv", "dwell-study-fe.csv") if a.out.endswith("dwell-study.csv") else a.out
        rows = dwell_at_conductance(prog, a.g_pb, out, a.layers)
    else:
        rows = dwell_study(prog, a.out, a.layers)
    keys = ["band_K", "plate_block_WK", "absorptivity", "block_offset_K", "argon_low_in_dwell", "result", "period_s",
            "dwell_share", "plate_max_C", "mean_absorbed_W", "build_10mm_h", "build_15mm_h", "argon_15mm_m3"]
    print(" | ".join(keys))
    for r in rows:
        print(" | ".join(str(r.get(k, "")) for k in keys))


def cmd_plot(a):
    from .plots import figure
    prog = load_program(a.program)
    n = int(round(a.height / prog.layer_mm))
    s = figure(prog, n, a.out)
    print(f"wrote {a.out}: {s['layers_done']} layers, {s['times_s']['total_s'] / 3600:.2f} h")


def cmd_interlock(a):
    from .interlock import report
    print(report())


def main(argv=None):
    p = argparse.ArgumentParser(prog="ftctl")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("simulate")
    s.add_argument("--layers", type=int, default=20)
    s.add_argument("--height", type=float, default=0.0, help="build height in mm (overrides --layers)")
    s.add_argument("--program", default=None, help="NPZ path, or 'synthetic'; default: the process worker's file")
    s.add_argument("--out", default="/tmp/ft-control/sim")
    s.add_argument("--name", default="build")
    s.add_argument("--speed", type=float, default=0.0, help="0 = as fast as possible, N = N x real time")
    s.add_argument("--seed", type=int, default=1)
    s.add_argument("--no-startup", action="store_true")
    s.add_argument("--no-finish", action="store_true", help="stop hot under argon after the last layer")
    s.add_argument("--no-vent", action="store_true")
    s.add_argument("--fault", action="append", help=f"NAME@T or NAME@layerK; names: {', '.join(FAULTS)}")
    s.set_defaults(fn=cmd_simulate)
    i = sub.add_parser("info")
    i.add_argument("--program", default=None)
    i.add_argument("--layers", type=int, default=5)
    i.set_defaults(fn=cmd_info)
    d = sub.add_parser("study-dwell", help="sweep the dwell band, plate-block conductance and absorptivity")
    d.add_argument("--program", default=None)
    d.add_argument("--layers", type=int, default=67)
    d.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parents[1] / "out" / "dwell-study.csv"))
    d.add_argument("--g-pb", type=float, default=None,
                   help="run the bands and block offsets at this plate-to-block conductance (W/K), e.g. the thermal FEA's; "
                        "writes out/dwell-study-fe.csv")
    d.set_defaults(fn=cmd_study_dwell)
    pl = sub.add_parser("plot", help="figure of one simulated build")
    pl.add_argument("--program", default=None)
    pl.add_argument("--height", type=float, default=2.0)
    pl.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parents[1] / "img" / "sim-build-2mm.png"))
    pl.set_defaults(fn=cmd_plot)
    il = sub.add_parser("interlock")
    il.set_defaults(fn=cmd_interlock)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
