"""Zaber X-VSR20A-E01 (piston) and X-LSM100B-E03 (recoater) through zaber-motion (ASCII protocol).

Both stages have built-in controllers, daisy-chained on 4-pin M8 Prev/Next cables that carry RS-232 and the 24-48 V
supply (pin 1 power, max 4 A; Zaber X-VSR-E and X-LSM-E manuals); 115,200 baud 8N1 by default. One supply feeds the
chain: the stages draw at most 0.95 A (X-VSR20A-E01) and 0.35 A (X-LSM100B-E03) (zaber.com specs, read 2026-11-27).
Warning flags starting with F are faults (FS stalled and stopped, FD driver disabled, FE limit error, FT excessive
twist, FQ encoder error, FM motor temperature, FV over/under voltage, FF critical system error, ...).
"""
from __future__ import annotations

from typing import Dict, Optional, Set

from .interfaces import Axis

DEVICES = {"piston": "X-VSR20A", "recoater": "X-LSM100B"}
SPEC = {"piston": (48.0, 200.0), "recoater": (104.0, 1000.0)}     # max speed mm/s (zaber.com), accel mm/s2 (estimate)


class ZaberAxis(Axis):
    def __init__(self, axis, name: str, vmax: float, amax: float):
        from zaber_motion import Units
        self.ax = axis
        self.name = name
        self.vmax = vmax
        self.amax = amax
        self.U = Units

    def home(self, wait: bool = True) -> None:
        self.ax.home(wait_until_idle=wait)

    def move_abs(self, pos_mm: float, speed: Optional[float] = None, accel: Optional[float] = None,
                 wait: bool = False) -> None:
        U = self.U
        self.ax.move_absolute(pos_mm, U.LENGTH_MILLIMETRES, wait_until_idle=wait,
                              velocity=min(speed or self.vmax, self.vmax), velocity_unit=U.VELOCITY_MILLIMETRES_PER_SECOND,
                              acceleration=accel or self.amax, acceleration_unit=U.ACCELERATION_MILLIMETRES_PER_SECOND_SQUARED)

    def position(self) -> float:
        return self.ax.get_position(self.U.LENGTH_MILLIMETRES)

    def busy(self) -> bool:
        return self.ax.is_busy()

    def stop(self) -> None:
        self.ax.stop(wait_until_idle=False)

    def flags(self) -> Set[str]:
        return set(self.ax.warnings.get_flags())

    def clear_flags(self) -> Set[str]:
        return set(self.ax.warnings.clear_flags())

    def set_run_current(self, fraction: float) -> None:
        """Scale the motor's run current (and so its thrust) for the hot piston stall-margin test (commission.py)."""
        st = self.ax.settings
        if not hasattr(self, "_i_run0"):
            self._i_run0 = st.get("driver.current.run")
        st.set("driver.current.run", self._i_run0 * fraction)

    def diagnostics(self) -> Dict[str, float]:
        st = self.ax.device.settings
        return dict(voltage_V=st.get("system.voltage"), temperature_C=st.get("system.temperature"))


def open_chain(port: str):
    """Open the daisy chain on a serial port and return {'piston': ZaberAxis, 'recoater': ZaberAxis}."""
    from zaber_motion.ascii import Connection
    conn = Connection.open_serial_port(port)
    devices = conn.detect_devices()
    found: Dict[str, ZaberAxis] = {}
    for dev in devices:
        for role, model in DEVICES.items():
            if model in dev.name:
                found[role] = ZaberAxis(dev.get_axis(1), role, *SPEC[role])
    missing = set(DEVICES) - set(found)
    if missing:
        conn.close()
        raise RuntimeError(f"Zaber chain on {port}: no {', '.join(sorted(missing))} among {[d.name for d in devices]}")
    found["_connection"] = conn
    return found
