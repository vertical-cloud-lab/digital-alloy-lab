"""A whole simulated build: start-up, 2 mm of layers, cool-down and vent, on one time base."""
import time

import numpy as np

from ftctl.logger import read_h5
from ftctl.states import S


def test_full_2mm_build(rig, program):
    r = rig()
    n = int(round(2.0 / program.layer_mm))                  # 67 layers of 30 um
    wall = time.time()
    s = r.run(n)
    wall = time.time() - wall
    assert s["result"] == "complete", s["fault"]
    assert s["layers_done"] == n
    assert abs(s["height_mm"] - n * program.layer_mm) < 1e-9
    assert wall < 60.0                                        # hours of machine time in seconds
    seq = s["states"]
    for a, b in [(S.PURGE, S.HEAT), (S.HEAT, S.HOME), (S.HOME, S.READY), (S.READY, S.PLATE_STEP),
                 (S.DONE, S.COOLDOWN), (S.COOLDOWN, S.VENT), (S.VENT, S.SAFE_TO_OPEN)]:
        assert seq.index(a.value) < seq.index(b.value)
    # one time base: every layer's list start is a rising edge of the RTC5 layer marker
    h = read_h5(s["files"]["hdf5"])
    lay, mk = h["layers"], h["markers"]
    rises = mk["t"][mk["edge"] == 1]
    assert len(rises) == n and len(lay) == n
    assert np.allclose(rises, lay["t_scan_start"], atol=1e-9)
    # each scan took its planned time on the card
    assert np.allclose(lay["scan_s"], lay["planned_scan_s"], atol=0.06)
    # the plate never ran away and every layer started inside the dwell band
    assert np.nanmax(h["samples"]["plate_C"]) < r.cfg.thermal.soft_limit_C
    band = r.cfg.thermal.setpoint_C + r.cfg.thermal.dwell_band_K
    assert np.all(lay["plate_C_scan_start"][1:] <= band + 0.5)
    # the lid may open only at air O2 and a cool plate
    assert r.w.o2_pct_reading * 1e4 >= r.cfg.gas.open_o2_ppm
    assert s["sim"]["trace_cell_in_air_s"] == 0.0              # the trace cell never saw air
    assert r.w.Tp < r.cfg.thermal.open_plate_C


def test_layer_sequence_and_recoat_moves(rig):
    r = rig()
    r.run(3, finish=False)
    seq = [h[2] for h in r.sup.sm.history]
    i = seq.index(S.READY)
    # first layer: no return stroke; later layers: return -> step -> spread -> scan -> log
    assert seq[i + 1] == S.PLATE_STEP
    later = [x for x in seq[i + 1:] if x in (S.RECOAT_RETURN, S.PLATE_STEP, S.SPREAD, S.SCAN, S.LOG)]
    assert later[:5] == [S.PLATE_STEP, S.SPREAD, S.SCAN, S.LOG, S.RECOAT_RETURN]
    mo = r.cfg.motion
    z_last = mo.piston_build_start_mm - 3 * r.prog.layer_mm
    assert abs(r.m.piston.position() - z_last) < 1e-6
    assert abs(r.m.recoater.position() - mo.stage_x(mo.park_right_x)) < 1e-6
    shots = r.m.camera.shots
    assert [(t, k) for _, t, k in shots] == [("powder", 0), ("scanned", 0), ("powder", 1), ("scanned", 1),
                                              ("powder", 2), ("scanned", 2)]


def test_cli_simulate(tmp_path, capsys):
    from ftctl.__main__ import main
    rc = main(["simulate", "--layers", "20", "--out", str(tmp_path), "--no-vent"])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"layers_done": 20' in out


def test_argon_low_flow_in_dwells_and_block_offset(rig):
    from ftctl.config import Config
    cfg = Config()
    cfg.thermal.block_offset_K = -20.0
    r = rig(cfg)
    s = r.run(12, finish=False)
    assert s["result"] == "complete", s["fault"]
    dwell = [x for x in r.log.samples if x["state"] == "DWELL"]
    scan = [x for x in r.log.samples if x["state"] == "SCAN"]
    # main flow off in dwells (low flow on), except the 2 s flow-settle window before a scan
    assert dwell and sum(x["argon"] == 0.0 for x in dwell) / len(dwell) > 0.7
    assert scan and all(x["argon"] == 1.0 for x in scan)            # full cross-flow whenever the beam is on
    assert abs(r.m.block.sv - 180.0) < 1e-9
    # the plate sheds more heat into a cooler block: shorter dwells than the default build
    r0 = rig()
    s0 = r0.run(12, finish=False)
    assert s["dwell_s"]["mean"] < 0.7 * s0["dwell_s"]["mean"]
