"""Start-up: purge to the O2 threshold, heat to 200 C, home hot, arm."""
from ftctl.config import Config
from ftctl.states import S


def test_startup_sequence(rig):
    r = rig()
    s = r.run(1, finish=False)
    assert s["result"] == "complete", s["fault"]
    g, th = r.cfg.gas, r.cfg.thermal
    ev = r.log.events
    t_state = {e["code"]: e["t"] for e in ev if e["kind"] == "state"}
    t_heat_on = next(e["t"] for e in ev if e["kind"] == "heaters" and e["code"] == "ON")
    # heaters start during the purge, once O2 < 1 %; the purge ends below o2_start_ppm
    assert t_state["PURGE"] < t_heat_on < t_state["HEAT"]
    samples = r.log.samples
    o2_at_heat_on = min((x for x in samples if x["t"] >= t_heat_on), key=lambda x: x["t"])["o2_ppm"]
    assert o2_at_heat_on < g.heat_below_ppm * 1.05
    at_heat = max((x for x in samples if x["t"] <= t_state["HEAT"]), key=lambda x: x["t"])
    assert at_heat["o2_ppm"] < g.o2_start_ppm * 1.1
    # the study expects 13-31 min to reach 1000 ppm (2-5 x perfect mixing at 20 L/min)
    assert 5 * 60 < s["times_s"]["purge_s"] < 31 * 60
    # homing happens hot, after the heat-up, and ends at the build start
    assert t_state["HEAT"] < t_state["HOME"] < t_state["READY"]
    at_home = [x for x in samples if t_state["HOME"] <= x["t"] <= t_state["READY"]]
    assert all(abs(x["plate_C"] - th.setpoint_C) < 4 for x in at_home)
    prompts = [e["code"] for e in ev if e["kind"] == "prompt"]
    assert prompts == ["safety_reset", "laser_start"]
    assert any(e["kind"] == "armed" and e["code"] == "EMON" for e in ev)


def test_purge_timeout_with_a_leak(rig):
    cfg = Config()
    cfg.gas.purge_timeout_s = 1800
    r = rig(cfg)
    r.w.extra_leak_Lpm = 2.0                       # floor ~15,000 ppm: the purge can never reach 1000 ppm
    s = r.run(1)
    r.assert_safe()
    assert s["fault"]["code"] == "O2_TIMEOUT"
    assert [h[2] for h in r.sup.sm.history][-3:] == [S.PURGE, S.SAFE_STOP, S.STOPPED]


def test_heat_timeout_with_weak_heaters(rig):
    cfg = Config()
    cfg.thermal.block_heater_W = 20.0              # cannot hold the block at 200 C against ~50 W of losses
    cfg.thermal.heat_timeout_s = 1800
    r = rig(cfg)
    s = r.run(1)
    r.assert_safe()
    assert s["fault"]["code"] == "HEAT_TIMEOUT"
