"""The real backends, driven against stand-ins: the RTC5 DLL, the IPG serial port, a Zaber axis, the Pi's GPIO."""
import threading
import time

import pytest

from ftctl.config import Config
from ftctl.hw import ipg as ipgmod
from ftctl.hw.rtc5 import FIELD_MAX, PROTOTYPES, FakeRtc5Dll, Rtc5Scan


# ---------------------------------------------------------------------------------------------------- RTC5
def test_rtc5_open_sequence_and_units(program):
    cfg = Config()
    d = FakeRtc5Dll(K=6000.0)
    card = Rtc5Scan(cfg, program.timing(), dll=d)
    card.open()
    n = d.names()
    order = ["init_rtc5_dll", "select_rtc", "load_program_file", "load_correction_file", "select_cor_table",
             "config_list", "set_laser_mode", "set_laser_control", "set_port_default", "write_da_1", "get_table_para",
             "enable_laser"]
    assert [x for x in n if x in order] == [x for x in order for _ in range(2 if x == "set_port_default" else 1)]
    assert card.K == 6000.0                                     # read from the correction table
    ctrl = dict(d.calls)["set_laser_control"][0]
    assert ctrl & (1 << 3) == 0                                 # LASERON active high
    assert all(ctrl & (1 << b) for b in (16, 17, 19, 20, 28))  # head PowerOK/TempOK suppress the laser and stop


def test_rtc5_layer_list(program):
    cfg = Config()
    d = FakeRtc5Dll(K=6000.0)
    card = Rtc5Scan(cfg, program.timing(), dll=d)
    card.open()
    d.calls.clear()
    layer = program.layer(0)
    lt = card.load_layer(layer, cfg.laser)
    calls = d.calls
    names = [c[0] for c in calls]
    assert names[:3] == ["set_start_list", "set_laser_pin_out_list", "set_trigger4"]
    i_end = names.index("set_end_of_list")
    assert calls[1][1] == (1,) and calls[i_end - 1] == ("set_laser_pin_out_list", (0,))
    assert names[i_end + 1:] == ["get_last_error"]
    tm = program.timing()
    args = dict(calls)
    # scanner delays in 10 us; laser delays in 0.5 us including the XY2-100 converter's 10 us
    assert args["set_scanner_delays"] == (30, 15, 5)
    assert args["set_laser_delays"] == (round((tm["laser_on_delay"] + 10e-6) / 0.5e-6),
                                       round((tm["laser_off_delay"] + 10e-6) / 0.5e-6))
    assert abs(args["set_jump_speed"][0] - tm["v_jump"] * 6000.0 / 1000.0) < 1e-6      # bits/ms
    # every coordinate inside the 20-bit real field; one mark_abs per segment
    for name, a in calls:
        if name in ("jump_abs", "mark_abs"):
            assert all(abs(v) <= FIELD_MAX for v in a)
    assert names.count("mark_abs") == len(layer) == lt["n_mark_list"]
    # power: hatch 250 W -> 62.5 % -> 6.25 V -> 2559; contour 150 W -> 37.5 % -> 3.75 V -> 1536 (12-bit, 0-10 V)
    das = [a[0] for nme, a in calls if nme == "write_da_1_list"]
    ps = program.meta["psets"][program.meta["parts"][0]["pset"]]
    assert card.da(ps["P_hatch"]) in das and das[-1] == 0
    assert card.da(250.0) == 2559 and card.da(150.0) == 1536 and card.da(0.0) == 0
    # mark speed bits/ms = mm/s * K / 1000
    speeds = sorted({a[0] for nme, a in calls if nme == "set_mark_speed"})
    assert any(abs(s - ps["v_hatch"] * 6.0) < 1e-6 for s in speeds)
    # every function used is in the prototype table (so load_dll sets its argtypes)
    assert set(names) <= set(PROTOTYPES)


def test_rtc5_run_status_and_trace(program):
    d = FakeRtc5Dll(busy_polls=2)
    card = Rtc5Scan(Config(), program.timing(), dll=d)
    card.open()
    card.load_layer(program.layer(1), None)
    card.start()
    states = [card.busy() for _ in range(4)]
    assert states == [True, True, False, False]
    assert card.head_status() == dict(pos_x=True, pos_y=True, temp=True, power=True)   # 0xFD: everything OK
    d.head = 0x7D                                                                        # power status bit 7 off
    assert not card.head_status()["power"]
    tr = card.trace()
    assert len(tr["t_s"]) == 10 and set(tr) >= {"laser_on", "x_mm", "y_mm", "da"}
    card.stop()
    assert d.names()[-2:] == ["stop_execution", "write_da_1"]


def test_rtc5_rejects_points_outside_the_field(program):
    card = Rtc5Scan(Config(), program.timing(), dll=FakeRtc5Dll(K=6000.0))
    with pytest.raises(Exception):
        card.bits((100.0, 0.0))                 # 600,000 bits > 524,287


def test_rtc5_dll_is_windows_only():
    from ftctl.hw.rtc5 import load_dll
    import sys
    if not sys.platform.startswith("win"):
        with pytest.raises(OSError):
            load_dll()


# ---------------------------------------------------------------------------------------------------- IPG
def test_ipg_commands_and_status():
    ser = ipgmod.FakeIpgSerial()
    las = ipgmod.IpgYlr(serial_obj=ser)
    las.open()
    assert las.identity == dict(firmware="1.0.147", serial="6103081", hours_min="1105")
    las.configure()
    las.emission(True)
    sta = las.status()
    assert sta & (1 << 2) and sta & (1 << 4) and sta & (1 << 12)
    assert "emission on or starting" in ipgmod.decode_sta(sta)
    assert ipgmod.decode_sta(4100) == ["emission on or starting", "modulation enabled"]   # the guide's example
    las.emission(False)
    assert not las.status() & (1 << 2)
    assert ser.log[3:8] == ["EEC", "EMOD", "DGM", "DLE", "ABF"]
    with pytest.raises(ipgmod.IpgError):
        las.command("XYZ")                                   # BCMD


def test_supervisor_maps_sta_bits():
    from ftctl.faults import Code, Fault
    from ftctl.supervisor import Supervisor
    with pytest.raises(Fault) as e:
        Supervisor._check_sta(None, 0.0, 1 << 3)
    assert e.value.code == Code.BACK_REFLECTION
    for bit in (1, 6, 19, 24, 25, 29, 30, 31):
        with pytest.raises(Fault) as e:
            Supervisor._check_sta(None, 0.0, 1 << bit)
        assert e.value.code == Code.LASER_FAULT
    Supervisor._check_sta(None, 0.0, (1 << 2) | (1 << 4) | (1 << 12) | (1 << 21))   # normal running: no fault


# ---------------------------------------------------------------------------------------------------- Zaber
class FakeZaberAxis:
    """The subset of zaber_motion.ascii.Axis that ZaberAxis uses."""

    def __init__(self):
        self.calls = []
        self.flags = {"WR"}
        self.pos = 0.0

        class W:
            def get_flags(w):
                return set(self.flags)

            def clear_flags(w):
                f = set(self.flags)
                self.flags.clear()
                return f
        self.warnings = W()

    def home(self, wait_until_idle=True):
        self.calls.append(("home", wait_until_idle))
        self.flags.discard("WR")

    def move_absolute(self, pos, unit, wait_until_idle=True, velocity=0, velocity_unit=None, acceleration=0,
                      acceleration_unit=None):
        self.calls.append(("move_absolute", pos, unit, velocity, velocity_unit, acceleration, acceleration_unit))
        self.pos = pos

    def get_position(self, unit):
        return self.pos

    def is_busy(self):
        return False

    def stop(self, wait_until_idle=True):
        self.calls.append(("stop", wait_until_idle))


def test_zaber_axis_units_and_flags():
    from zaber_motion import Units
    from ftctl.hw.zaber import ZaberAxis
    fa = FakeZaberAxis()
    ax = ZaberAxis(fa, "recoater", 104.0, 1000.0)
    ax.home()
    ax.move_abs(66.4, speed=500.0)
    c = fa.calls[-1]
    assert c[1] == 66.4 and c[2] == Units.LENGTH_MILLIMETRES
    assert c[3] == 104.0 and c[4] == Units.VELOCITY_MILLIMETRES_PER_SECOND       # clamped to the stage's maximum
    assert c[6] == Units.ACCELERATION_MILLIMETRES_PER_SECOND_SQUARED
    assert ax.position() == 66.4
    fa.flags |= {"FS"}
    assert "FS" in ax.flags()
    ax.stop()
    assert fa.calls[-1] == ("stop", False)


# ---------------------------------------------------------------------------------------------------- Pi node
def test_pi_node_over_tcp_with_mock_pins():
    from gpiozero.pins.mock import MockFactory
    from ftctl.hw.pinode import IN_PINS, OUT_PINS, PiIoNode, RemoteIoNode, RemoteZone, serve

    class Zone:
        name = "plate"

        def __init__(self):
            self.sv, self.on = 0.0, False

        def pv(self):
            return 199.6

        def set_sv(self, c):
            self.sv = c

        def run(self, on):
            self.on = on

    f = MockFactory()
    volts = {0: 4.0 * 250 / 1000 + 0.05 * 250 / 1000 * 0, 1: 1.0, 2: 0.0}     # 4 mA = 0 ppm; 4 mA; 0 mA (open loop)
    zone = Zone()
    node = PiIoNode(pin_factory=f, tc_reader=lambda ch: [41.0, 25.0, 38.5, -9999.0][ch],
                    volt_reader=lambda ch: volts[ch], zones={"plate": zone}, watchdog_s=0.6)
    srv = serve(node, "127.0.0.1", 0)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        pc = RemoteIoNode("127.0.0.1", port)
        pc.set("ARGON", True)
        pc.set("HEAT_EN", True)
        assert f.pin(OUT_PINS["ARGON"]).state and f.pin(OUT_PINS["HEAT_EN"]).state
        f.pin(IN_PINS["SAFETY_OK"]).drive_low()                 # 24 V present -> opto pulls the pin low
        f.pin(IN_PINS["LIMIT_OK"]).drive_high()
        s = pc.snapshot()
        assert s["SAFETY_OK"] is True and s["LIMIT_OK"] is False
        assert s["window"] == 41.0 and s["stage"] != s["stage"]  # open thermocouple -> NaN
        assert s["o2_ppm"] == 0.0 and s["room_o2_pct"] != s["room_o2_pct"]   # 0 mA -> NaN (broken loop)
        rz = RemoteZone(pc, "plate")
        rz.set_sv(200.0)
        rz.run(True)
        assert zone.sv == 200.0 and zone.on and rz.pv() == 199.6
        # watchdog: no request for 0.6 s -> HEAT_EN drops on the Pi by itself; argon stays on
        time.sleep(1.0)
        assert not f.pin(OUT_PINS["HEAT_EN"]).state
        assert f.pin(OUT_PINS["ARGON"]).state
        pc.close()
    finally:
        srv.shutdown()
        srv.server_close()
        node.close()


def test_solo_modbus_registers():
    from ftctl.hw.pinode import SoloPid

    class Ins:
        def __init__(self):
            self.regs = {0x1000: 1996, 0x1001: 0}
            self.writes = []

        def read_register(self, addr, decimals, functioncode=3, signed=False):
            return self.regs[addr]

        def write_register(self, addr, value, decimals, functioncode=16):
            self.writes.append((addr, value, functioncode))
            self.regs[addr] = value

    ins = Ins()
    z = SoloPid("/dev/null", 1, "plate", instrument=ins)
    assert z.pv() == 199.6
    z.set_sv(200.0)
    z.run(True)
    z.run(False)
    assert ins.writes == [(0x1001, 2000, 6), (0x1001, 0, 6)]
    ins.regs[0x1000] = 0x8002                                   # SOLO: input sensor error
    assert z.pv() != z.pv()
