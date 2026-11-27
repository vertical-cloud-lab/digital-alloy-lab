"""Parameter studies on the simulated machine.

dwell_study: the plate takes the laser's heat (absorptivity x ~720 J a layer for the process worker's first-coupon
program) and can only pass it to the well block across the 0.1 mm argon gap (plate_block_WK) or lose it to the box.
The supervisor holds each layer until the plate is back under setpoint + dwell_band_K. This sweeps the band, the gap
conductance and the absorptivity, and reports the steady layer period and the build times it implies.
"""
from __future__ import annotations

import csv
import pathlib
import tempfile

from .clock import SimClock
from .config import Config
from .hw.sim import make_sim_machine
from .logger import BuildLog
from .supervisor import Supervisor


def run_case(prog, n_layers: int, band: float, g_pb: float, absorptivity: float, block_offset: float = 0.0,
             argon_save: bool = True, soft_limit: float = 260.0) -> dict:
    cfg = Config()
    cfg.thermal.block_offset_K = block_offset
    cfg.argon_low_in_dwell = argon_save
    cfg.thermal.dwell_band_K = band
    cfg.thermal.plate_block_WK = g_pb
    cfg.thermal.absorptivity = absorptivity
    cfg.thermal.soft_limit_C = soft_limit           # the study looks at where the plate settles, not at the trip
    cfg.thermal.limit_C = soft_limit + 15
    cfg.camera = False
    clock = SimClock()
    m = make_sim_machine(cfg, clock, prog.timing())
    with tempfile.TemporaryDirectory() as d:
        log = BuildLog(d, clock)
        sup = Supervisor(m, cfg, prog, log, clock)
        s = sup.run(list(range(n_layers)), startup=True, finish=False)
        rows = [r for r in log.layers if r.get("complete")]
    if s["result"] != "complete":
        return dict(band_K=band, plate_block_WK=g_pb, absorptivity=absorptivity, block_offset_K=block_offset,
                    result=s["fault"]["code"])
    tail = rows[len(rows) // 2:]
    period = (tail[-1]["t_start"] - tail[0]["t_start"]) / (len(tail) - 1)
    no_dwell = sum(r["recoat_s"] + r["scan_s"] for r in tail) / len(tail)
    plate = [x["plate_C"] for x in log.samples if x["t"] >= rows[0]["t_start"]]
    lm = prog.layer_mm
    argon_build_L = s["sim"]["argon_used_L"] - s["times_s"]["startup_s"] / 60.0 * cfg.gas.build_flow_Lpm
    return dict(band_K=band, plate_block_WK=g_pb, absorptivity=absorptivity, block_offset_K=block_offset,
                argon_low_in_dwell=argon_save, result="complete",
                period_s=round(period, 2), period_without_dwell_s=round(no_dwell, 2),
                dwell_share=round(1 - no_dwell / period, 3), plate_max_C=round(max(plate), 1),
                build_2mm_h=round(period * round(2 / lm) / 3600, 2), build_10mm_h=round(period * round(10 / lm) / 3600, 2),
                build_15mm_h=round(period * round(15 / lm) / 3600, 2),
                mean_absorbed_W=round(absorptivity * sum(r["energy_J"] for r in tail) / len(tail) / period, 1),
                argon_15mm_m3=round(argon_build_L / len(rows) * round(15 / lm) / 1000.0, 2))


def dwell_study(prog, out_csv, n_layers: int = 67):
    cases = [(b, 0.9, 0.45) for b in (3.0, 5.0, 10.0, 20.0)]
    cases += [(5.0, g, 0.45) for g in (2.0, 5.0)]
    cases += [(5.0, 0.9, a) for a in (0.3, 0.6)]
    cases += [(5.0, 0.9, 0.45, off) for off in (-10.0, -20.0)]
    cases += [(20.0, 2.0, 0.45), (10.0, 0.9, 0.45, -20.0)]
    cases += [(5.0, 0.9, 0.45, 0.0, False)]          # the same build without the low flow in dwells
    rows = [run_case(prog, n_layers, *c) for c in cases]
    out_csv = pathlib.Path(out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(rows)
    return rows
