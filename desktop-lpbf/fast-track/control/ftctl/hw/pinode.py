"""Raspberry Pi 5 I/O node: relays, opto-isolated 24 V inputs, slow thermocouples, 4-20 mA inputs and the two PID
controllers, served to the supervisor on the PC as JSON lines over TCP.

On the Pi:   python -m ftctl.hw.pinode --host <the Pi's address on the direct PC link> --port 5055
On the PC:   RemoteIoNode(host, 5055) and RemoteZone(node, "plate"), RemoteZone(node, "block")

Hardware (io-list.csv): gpiozero with the lgpio pin factory (the only one that works on a Pi 5, gpiozero docs);
MCC 134 thermocouple HAT (isolated inputs; daqhats returns -9999.0 for an open thermocouple) and MCC 128 analog HAT
(+/-10 V; 4-20 mA through 250 ohm shunts = 1-5 V); the HATs use GPIO 8-11, 12, 13 and 26 (MCC electrical specs),
which the pin map below avoids. Two AutomationDirect SOLO SL4848-VR-D PID controllers on RS-485 Modbus RTU: PV at
0x1000 (read only; 0x8002-0x8007 = sensor errors), SV at 0x1001 in 0.1 C, written only with P3-12 CoSH = ON (SOLO user
manual). Stopping a zone writes SV = 0 C (no unconfirmed run/stop register is used); K1 cuts the heater supply anyway.

Watchdog: if the PC sends nothing for watchdog_s, the node drops HEAT_EN (K1), the vibrator and the LEDs on its own.
Argon is left as it is: inert gas over hot powder is the safe state.
"""
from __future__ import annotations

import json
import math
import socket
import socketserver
import threading
import time
from typing import Callable, Dict, Optional

from .interfaces import ANALOG, INPUTS, OUTPUTS, TEMPS, HeaterZone, IoNode

# BCM numbers. Outputs drive a ULN2803A into 24 V DIN-rail interface relays (active high); inputs come from an
# opto-isolated 24 V input board whose outputs pull the pin low when the 24 V signal is present (active low).
OUT_PINS = {"ARGON": 17, "ARGON_LOW": 27, "VENT": 22, "TRACE_SAMPLE": 23, "VIBRATOR": 24, "HEAT_EN": 25, "LEDS": 4,
            "BEACON": 18}
IN_PINS = {"SAFETY_OK": 14, "LASER_PS_ACTIVE": 15, "LASER_EMISSION": 16, "LASER_READY": 19, "LIMIT_OK": 20,
           "ROOM_O2_OK": 21, "WATER_OK": 2, "LID_CLOSED": 3, "K1_ON": 7}   # GPIO 7 needs dtoverlay=spi0-1cs
TC_CHANNELS = {"window": 0, "beam_tube": 1, "box_air": 2, "stage": 3}      # MCC 134, type K
MA_CHANNELS = {"o2_ppm": (0, 0.0, 10_000.0), "o2_pct": (1, 0.0, 25.0), "room_o2_pct": (2, 0.0, 25.0)}  # MCC 128
OPEN_TC = -9999.0


def ma_to_value(volts: float, lo: float, hi: float, shunt: float = 250.0) -> float:
    """4-20 mA through a shunt -> engineering value; NaN below 3.6 mA (open loop or a failed transmitter)."""
    ma = volts / shunt * 1000.0
    if ma < 3.6:
        return float("nan")
    return lo + (hi - lo) * (min(ma, 20.5) - 4.0) / 16.0


class SoloPid(HeaterZone):
    """AutomationDirect SOLO over Modbus RTU (minimalmodbus)."""

    PV, SV = 0x1000, 0x1001

    def __init__(self, port: str, address: int, name: str, instrument=None):
        if instrument is None:
            import minimalmodbus
            instrument = minimalmodbus.Instrument(port, address)
            instrument.serial.baudrate = 9600
            instrument.serial.timeout = 0.2
        self.ins = instrument
        self.name = name
        self.sv = 0.0

    def pv(self) -> float:
        raw = self.ins.read_register(self.PV, 0, functioncode=3, signed=False)
        if 0x8002 <= raw <= 0x8007:
            return float("nan")
        if raw >= 0x8000:
            raw -= 0x10000
        return raw / 10.0

    def set_sv(self, celsius: float) -> None:
        self.sv = celsius

    def run(self, on: bool) -> None:
        self.ins.write_register(self.SV, int(round((self.sv if on else 0.0) * 10)), 0, functioncode=6)


class PiIoNode(IoNode):
    def __init__(self, pin_factory=None, tc_reader: Optional[Callable[[int], float]] = None,
                 volt_reader: Optional[Callable[[int], float]] = None, zones: Optional[Dict[str, HeaterZone]] = None,
                 watchdog_s: float = 5.0):
        from gpiozero import DigitalInputDevice, OutputDevice
        kw = {"pin_factory": pin_factory} if pin_factory is not None else {}
        self.outs = {n: OutputDevice(p, active_high=True, initial_value=False, **kw) for n, p in OUT_PINS.items()}
        self.ins = {n: DigitalInputDevice(p, pull_up=True, **kw) for n, p in IN_PINS.items()}
        self.tc_reader = tc_reader or self._mcc134()
        self.volt_reader = volt_reader or self._mcc128()
        self.zones = zones or {}
        self.watchdog_s = watchdog_s
        self.last_request = time.monotonic()
        self.tripped = False
        self._stop = threading.Event()
        threading.Thread(target=self._watchdog, daemon=True).start()

    @staticmethod
    def _mcc134():
        from daqhats import TcTypes, mcc134
        hat = mcc134(0)
        for ch in TC_CHANNELS.values():
            hat.tc_type_write(ch, TcTypes.TYPE_K)
        return hat.t_in_read

    @staticmethod
    def _mcc128():
        from daqhats import AnalogInputMode, AnalogInputRange, mcc128
        hat = mcc128(1)
        hat.a_in_mode_write(AnalogInputMode.SE)
        hat.a_in_range_write(AnalogInputRange.BIP_10V)
        return lambda ch: hat.a_in_read(ch)

    def _watchdog(self):
        while not self._stop.wait(0.2):
            if time.monotonic() - self.last_request > self.watchdog_s and not self.tripped:
                for n in ("HEAT_EN", "VIBRATOR", "LEDS"):
                    self.outs[n].off()
                self.tripped = True

    def touch(self):
        self.last_request = time.monotonic()
        self.tripped = False

    def set(self, name, on):
        self.outs[name].on() if on else self.outs[name].off()

    def get(self, name):
        return bool(self.ins[name].value)               # pull_up=True: gpiozero reads a low pin (24 V present) as 1

    def temps(self):
        out = {}
        for k, ch in TC_CHANNELS.items():
            v = self.tc_reader(ch)
            out[k] = float("nan") if v <= OPEN_TC + 1 else float(v)
        return out

    def analog(self):
        return {k: ma_to_value(self.volt_reader(ch), lo, hi) for k, (ch, lo, hi) in MA_CHANNELS.items()}

    def close(self):
        self._stop.set()
        for d in list(self.outs.values()) + list(self.ins.values()):
            d.close()


class _Handler(socketserver.StreamRequestHandler):
    def handle(self):
        node: PiIoNode = self.server.node
        for line in self.rfile:
            try:
                req = json.loads(line)
                node.touch()
                op = req["op"]
                if op == "set":
                    node.set(req["name"], bool(req["on"]))
                    data = None
                elif op == "get":
                    data = node.get(req["name"])
                elif op == "snapshot":
                    data = node.snapshot()
                elif op == "zone":
                    z = node.zones[req["zone"]]
                    cmd = req["cmd"]
                    if cmd == "pv":
                        data = z.pv()
                    elif cmd == "sv":
                        z.set_sv(float(req["value"]))
                        data = None
                    elif cmd == "run":
                        z.run(bool(req["on"]))
                        data = None
                    else:
                        raise ValueError(cmd)
                elif op == "ping":
                    data = "pong"
                else:
                    raise ValueError(op)
                rep = {"ok": True, "data": data}
            except Exception as e:                       # noqa: BLE001
                rep = {"ok": False, "error": repr(e)}
            self.wfile.write((json.dumps(rep, allow_nan=True) + "\n").encode())


def serve(node: PiIoNode, host: str = "127.0.0.1", port: int = 5055):
    """Serve the node. Bind to the direct PC link's address, never to an open network: whoever can connect can switch
    the heater contactor and the gas valves."""
    srv = socketserver.ThreadingTCPServer((host, port), _Handler)
    srv.daemon_threads = True
    srv.node = node
    return srv


class RemoteIoNode(IoNode):
    """The PC side of the link."""

    def __init__(self, host: str, port: int = 5055, timeout: float = 1.0):
        self.addr = (host, port)
        self.timeout = timeout
        self.sock = None
        self.f = None

    def _call(self, **req):
        for attempt in (1, 2):
            try:
                if self.sock is None:
                    self.sock = socket.create_connection(self.addr, timeout=self.timeout)
                    self.f = self.sock.makefile("rwb")
                self.f.write((json.dumps(req) + "\n").encode())
                self.f.flush()
                line = self.f.readline()
                if not line:
                    raise ConnectionError("I/O node closed the link")
                rep = json.loads(line)
                if not rep["ok"]:
                    raise RuntimeError(rep["error"])
                return rep["data"]
            except (OSError, ConnectionError):
                self.close()
                if attempt == 2:
                    raise ConnectionError(f"I/O node at {self.addr[0]}:{self.addr[1]} not answering")

    def set(self, name, on):
        self._call(op="set", name=name, on=bool(on))

    def get(self, name):
        return self._call(op="get", name=name)

    def snapshot(self):
        d = self._call(op="snapshot")
        return {k: (float("nan") if v is None else v) for k, v in d.items()}

    def temps(self):
        s = self.snapshot()
        return {k: s[k] for k in TEMPS}

    def analog(self):
        s = self.snapshot()
        return {k: s[k] for k in ANALOG}

    def heartbeat(self):
        self._call(op="ping")

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        finally:
            self.sock = self.f = None


class RemoteZone(HeaterZone):
    def __init__(self, node: RemoteIoNode, name: str):
        self.node = node
        self.name = name

    def pv(self):
        v = self.node._call(op="zone", zone=self.name, cmd="pv")
        return float("nan") if v is None or (isinstance(v, float) and math.isnan(v)) else float(v)

    def set_sv(self, celsius):
        self.node._call(op="zone", zone=self.name, cmd="sv", value=celsius)

    def run(self, on):
        self.node._call(op="zone", zone=self.name, cmd="run", on=bool(on))


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(prog="ftctl.hw.pinode")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=5055)
    p.add_argument("--rs485", default="/dev/ttyUSB0")
    a = p.parse_args(argv)
    zones = {"plate": SoloPid(a.rs485, 1, "plate"), "block": SoloPid(a.rs485, 2, "block")}
    node = PiIoNode(zones=zones)
    srv = serve(node, a.host, a.port)
    try:
        srv.serve_forever()
    finally:
        node.close()


if __name__ == "__main__":
    main()


__all__ = ["PiIoNode", "RemoteIoNode", "RemoteZone", "SoloPid", "serve", "OUT_PINS", "IN_PINS", "INPUTS", "OUTPUTS"]
