"""Each fault, injected into the simulated machine, ends in a safe stop with the right code."""
import math

import pytest

from ftctl.config import Config
from ftctl.states import S


def run_with(rig, hook_layer, fn, n=8, cfg=None, finish=False):
    r = rig(cfg)
    r.w.on_layer(hook_layer, fn)            # fires when that layer's list starts (mid-scan for anything fast)
    r.run(n, finish=finish)
    return r


def test_o2_rises_during_a_scan(rig):
    cfg = Config()
    cfg.gas.analyzer_t90_s = 1.0            # a fast cell so the trip lands inside the 3 s list
    r = run_with(rig, 3, lambda w: setattr(w, "extra_leak_Lpm", 60.0), cfg=cfg)
    r.assert_safe()
    assert r.summary["fault"]["code"] == "O2_HIGH"
    bad = [x for x in r.log.layers if x["layer"] == 3][0]
    assert bad["complete"] == 0.0 and "scan_s" not in bad          # the layer is logged as aborted
    assert r.m.io.out["ARGON"]                                      # argon keeps flowing


def test_o2_hold_between_layers_then_resume(rig):
    r = rig()
    # a short leak after layer 2's list: O2 climbs over 1000 ppm, the next layer holds, then the purge wins
    def leak(w):
        w.extra_leak_Lpm = 0.5
        w.at(w.clock.now() + 150.0, lambda w2: setattr(w2, "extra_leak_Lpm", 0.0))
    r.w.on_layer(2, leak)
    s = r.run(6, finish=False)
    assert s["result"] == "complete", s["fault"]
    assert s["hold_s"]["total"] > 30.0
    assert S.HOLD.value in s["states"]


def test_lid_opened_mid_scan(rig):
    r = run_with(rig, 4, lambda w: setattr(w, "lid_closed", False))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "INTERLOCK_OPEN"
    assert not r.w.g9se and not r.w.laser_ps          # the hard-wired chain dropped the laser on its own


def test_estop(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "estop_ok", False))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "INTERLOCK_OPEN"
    assert not r.m.io.get("K1_ON")                    # the E-stop's third contact dropped the heater contactor


def test_stage_stall(rig):
    r = run_with(rig, 3, lambda w: setattr(w.axes["piston"], "stall_next", True))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "STAGE_FAULT"
    assert "FS" in r.summary["fault"]["message"] or "wanted" in r.summary["fault"]["message"]


def test_thermocouple_open(rig):
    r = run_with(rig, 3, lambda w: w.tc_open.add("plate"))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "TC_OPEN"


@pytest.mark.parametrize("name", ["window", "beam_tube", "box_air"])
def test_other_thermocouples_open(rig, name):
    r = run_with(rig, 2, lambda w: w.tc_open.add(name))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "TC_OPEN"


def test_plate_overtemperature_from_a_shorted_ssr(rig):
    r = run_with(rig, 2, lambda w: w.heater_stuck_on.add("plate"))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "PLATE_OVERTEMP"
    # K1 (software, HEAT_EN) cut the shorted SSR's supply before the CN708 limit was needed
    assert not r.w.cn708_tripped
    assert r.w.Tp < r.cfg.thermal.limit_C


def test_cn708_limit_without_the_supervisor(program, tmp_path):
    """The hardware alone: SSR shorted, nobody watching. The CN708 opens K2 and the plate stops near the limit."""
    from tests.conftest import Rig
    r = Rig(program, tmp_path)
    w = r.w
    r.m.io.set("HEAT_EN", True)
    for z in (r.m.plate, r.m.block):
        z.set_sv(200.0)
        z.run(True)
    w.heater_stuck_on.add("plate")
    peak = 0.0
    for _ in range(int(3600 / 0.5)):
        r.clock.sleep(0.5)
        peak = max(peak, w.Tp)
    assert w.cn708_tripped
    assert r.cfg.thermal.limit_C < peak < r.cfg.thermal.limit_C + 10.0
    assert w.Tp < 100.0                                       # and it cooled once K2 opened


def test_back_reflection(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "laser_bits", 1 << 3))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "BACK_REFLECTION"


def test_laser_overheat(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "laser_bits", 1 << 1))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "LASER_FAULT"


def test_scanner_power_fault(rig):
    r = run_with(rig, 2, lambda w: w.head.update(power=False))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "SCANNER_FAULT"


def test_fouled_cover_slide_heats_the_window_ring(rig):
    r = run_with(rig, 1, lambda w: setattr(w, "cover_slide_fouling", 0.6), n=60)
    r.assert_safe()
    assert r.summary["fault"]["code"] == "WINDOW_HOT"
    assert "WINDOW_WARM" in r.summary["warnings"]


def test_stray_beam(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "stray_W", 40.0), n=40)
    r.assert_safe()
    assert r.summary["fault"]["code"] == "STRAY_BEAM"


def test_room_oxygen_low(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "room_o2_pct", 19.0))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "ROOM_O2_LOW"
    assert not r.m.io.out["ARGON"] and not r.m.io.out["ARGON_LOW"]


def test_io_link_lost(rig):
    r = rig()
    r.w.on_layer(2, lambda w: setattr(w.io, "link_ok", False))
    s = r.run(6, finish=False)
    assert s["fault"]["code"] == "IO_LINK_LOST"
    assert s["final_state"] == "STOPPED"
    assert not r.w.emission and not r.w.list_busy


def test_graceful_operator_stop(rig):
    r = rig()
    r.w.on_layer(3, lambda w: r.sup.request_stop(graceful=True))
    s = r.run(8, finish=False)
    assert s["fault"]["code"] == "OPERATOR_STOP"
    assert s["layers_done"] == 4                    # layer 3 was finished first
    assert not r.w.emission


def test_no_fault_leaves_nan_in_the_log(rig):
    r = rig()
    s = r.run(4, finish=False)
    assert s["result"] == "complete"
    assert all(not math.isnan(x["plate_C"]) for x in r.log.samples)


def test_scan_head_water_lost(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "water_ok", False))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "COOLING_FAULT"


def test_cn708_limit_trip_seen_by_the_supervisor(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "cn708_tripped", True))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "LIMIT_TRIPPED"


def test_dwell_timeout(rig):
    cfg = Config()
    cfg.thermal.dwell_max_s = 5.0                 # every dwell here lasts ~20 s
    r = rig(cfg)
    s = r.run(8, finish=False)
    r.assert_safe()
    assert s["fault"]["code"] == "DWELL_TIMEOUT"


def test_box_air_too_hot_for_the_stages(rig):
    def fan_fails(w):
        w.box_fan_failed = True
        w.box_extra_K = 15.0                     # still air plus a hot stage motor (estimate)
    r = run_with(rig, 2, fan_fails, n=60)
    r.assert_safe()
    assert r.summary["fault"]["code"] == "BOX_AIR_HOT"


def test_rtc_error(rig):
    r = run_with(rig, 2, lambda w: setattr(w, "rtc_error", 0x10))
    r.assert_safe()
    assert r.summary["fault"]["code"] == "RTC_ERROR"


def test_driver_exception_is_a_safe_stop(rig):
    r = rig()
    cam = r.m.camera
    orig = cam.capture

    def capture(tag, layer):
        if layer == 2:
            raise RuntimeError("camera driver crashed")
        return orig(tag, layer)
    cam.capture = capture
    r.run(6, finish=False)
    r.assert_safe()
    assert r.summary["fault"]["code"] == "INTERNAL_ERROR"


@pytest.mark.parametrize("loop,code", [("room_o2_pct", "ROOM_O2_LOW"), ("o2_pct", "O2_HIGH"), ("o2_ppm", "O2_HIGH")])
def test_lost_oxygen_signal(rig, loop, code):
    r = run_with(rig, 2, lambda w: w.loops_broken.add(loop))
    r.assert_safe()
    assert r.summary["fault"]["code"] == code and "signal lost" in r.summary["fault"]["message"]
