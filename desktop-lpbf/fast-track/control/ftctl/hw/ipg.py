"""IPG YLR fibre laser over RS-232 (pyserial).

Command set and status bits from IPG's YLR-series user guide (the 24-pin-connector generation), "Computer Interface /
Commands", public copy: https://manualedistruzioni.it/ipg/measuring-instrument/ylr-series/user-manual/20cai (pp. 56-64):
RS-232 3-wire, 57,600 baud, 8 data bits, 1 stop bit, no parity, no flow control; every command and reply ends with CR;
a reply echoes the command, and a returned value follows ': '; an unknown command returns 'BCMD'.
Back reflection is STA bit 3 in this guide and in the 2009 YLR-200-AC and 2012 YLR guides (research notes).

The unit here is a 2015 YLR-400-SM-EOS. Its front/rear panel shows INTERLOCK, MODULATION INPUT and RESET connectors, not
the 24-pin and 8-pin connectors of the guide, so its serial port, baud rate and command set must be confirmed on
arrival (README, arrival checks). This driver only reads status and switches emission; the beam's power and gate come
from the RTC5's ANALOG OUT1 and LASERON.
"""
from __future__ import annotations

from typing import Dict, List

from .interfaces import Laser

STA_BITS = {
    1: "overheat", 2: "emission on or starting", 3: "high back reflection", 4: "external control enabled",
    6: "module disconnected", 8: "aiming beam on", 11: "power supply off", 12: "modulation enabled",
    15: "emission in 3 s start-up", 16: "gate mode enabled", 18: "hardware emission control enabled",
    19: "power supply failure", 20: "front panel locked", 21: "keyswitch in REM", 24: "low temperature",
    25: "power supply failure (2)", 27: "hardware aiming beam control enabled", 29: "critical error",
    30: "optical interlock active", 31: "average power too high",
}


def decode_sta(word: int) -> List[str]:
    return [name for bit, name in sorted(STA_BITS.items()) if word & (1 << bit)]


class IpgError(RuntimeError):
    pass


class IpgYlr(Laser):
    def __init__(self, port: str = "COM3", baud: int = 57600, timeout: float = 0.5, serial_obj=None):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.ser = serial_obj

    def open(self) -> None:
        if self.ser is None:
            import serial                                      # pyserial
            self.ser = serial.Serial(self.port, self.baud, bytesize=8, parity="N", stopbits=1, timeout=self.timeout,
                                     xonxoff=False, rtscts=False)
        self.identity = dict(firmware=self.query("RFV"), serial=self.query("RSN"), hours_min=self.query("RET"))

    def command(self, cmd: str) -> str:
        """Send one command; return the reply without the CR. Raises on BCMD or ERR."""
        self.ser.reset_input_buffer()
        self.ser.write((cmd + "\r").encode("ascii"))
        reply = self.ser.read_until(b"\r").decode("ascii", "replace").strip()
        if not reply:
            raise IpgError(f"{cmd}: no reply in {self.timeout} s")
        if reply.startswith("BCMD") or reply.startswith("ERR"):
            raise IpgError(f"{cmd}: {reply}")
        return reply

    def query(self, cmd: str) -> str:
        reply = self.command(cmd)
        return reply.split(":", 1)[1].strip() if ":" in reply else reply

    # Laser interface
    def configure(self) -> None:
        """Analog power from the RTC5 (EEC), gate from LASERON (EMOD), no internal pulse generator (DGM), emission
        switched over RS-232 (DLE), guide laser off (ABF)."""
        for c in ("EEC", "EMOD", "DGM", "DLE", "ABF"):
            self.command(c)

    def emission(self, on: bool) -> None:
        self.command("EMON" if on else "EMOFF")

    def status(self) -> int:
        return int(self.query("STA"))

    def reset_errors(self) -> None:
        self.command("RERR")

    def guide(self, on: bool) -> None:
        self.command("ABN" if on else "ABF")

    def readings(self) -> Dict[str, str]:
        """Case temperature, output power, error code, set point (for the log at each layer)."""
        return dict(temp_C=self.query("RCT"), power=self.query("ROP"), error=self.query("RMEC"),
                    setpoint_pct=self.query("RCS"))

    def close(self) -> None:
        if self.ser is not None:
            try:
                self.emission(False)
            finally:
                self.ser.close()


class FakeIpgSerial:
    """A YLR that answers like the guide's examples, for tests."""

    def __init__(self):
        self.sta = (1 << 21) | (1 << 11)            # REM, power supply off
        self.out = b""
        self.log = []
        self.ps_active = True

    def reset_input_buffer(self):
        self.out = b""

    def write(self, data: bytes):
        cmd = data.decode().strip()
        self.log.append(cmd)
        name = cmd.split()[0].upper()
        if name == "STA":
            r = f"STA: {self.sta}"
        elif name == "EMON":
            self.sta |= 1 << 2
            r = "EMON"
        elif name == "EMOFF":
            self.sta &= ~(1 << 2)
            r = "EMOFF"
        elif name in ("EEC", "EMOD", "DGM", "DLE", "ABF", "ABN", "RERR"):
            if name == "EEC":
                self.sta |= 1 << 4
            if name == "EMOD":
                self.sta |= 1 << 12
            r = name
        elif name in ("RFV", "RSN", "RET", "RCT", "ROP", "RMEC", "RCS"):
            r = {"RFV": "RFV: 1.0.147", "RSN": "RSN: 6103081", "RET": "RET: 1105", "RCT": "RCT: 34.5",
                 "ROP": "ROP: Off", "RMEC": "RMEC: 0", "RCS": "RCS: 56.7"}[name]
        else:
            r = "BCMD"
        self.out = (r + "\r").encode()

    def read_until(self, term=b"\r"):
        o, self.out = self.out, b""
        return o

    def close(self):
        pass
