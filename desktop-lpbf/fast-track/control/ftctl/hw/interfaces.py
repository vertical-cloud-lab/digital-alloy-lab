"""Small hardware interfaces the supervisor talks to. Each has a simulated backend (sim.py) and a real one."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Set

# Names of the Pi I/O node's channels (see io-list.csv for the wiring)
OUTPUTS = ("ARGON", "ARGON_LOW", "VENT", "VIBRATOR", "HEAT_EN", "LEDS", "BEACON")
INPUTS = ("SAFETY_OK", "ESTOP_OK", "LID_CLOSED", "LASER_PS_ACTIVE", "LASER_EMISSION", "LASER_READY", "LIMIT_OK",
          "ROOM_O2_OK", "K1_ON")
TEMPS = ("window", "beam_tube", "box_air", "stage")
ANALOG = ("o2_ppm", "room_o2_pct")


class ScanCard(ABC):
    """SCANLAB RTC5 (or its simulation): one list per layer."""

    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def load_layer(self, layer, laser_cfg) -> dict:
        """Write the layer's list (jumps, marks, power, speed, delays, markers). Returns its planned timing."""

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def busy(self) -> bool: ...

    @abstractmethod
    def stop(self) -> None:
        """stop_execution: laser signals off now, analog out to its default (0 V), marker low."""

    @abstractmethod
    def head_status(self) -> Dict[str, bool]:
        """{'power': ..., 'temp': ..., 'pos_x': ..., 'pos_y': ...} from the XY2-100 status word."""

    @abstractmethod
    def last_error(self) -> int: ...

    def list_time(self) -> Optional[float]:
        """The card's own measurement of the last list (save_and_restart_timer / get_time), if any."""
        return None

    def trace(self) -> Optional[dict]:
        """Signals recorded on the card during the last list (set_trigger4 / get_waveform), if any."""
        return None

    def close(self) -> None:
        pass


class Laser(ABC):
    """IPG YLR over RS-232 (or its simulation). Power and gate come from the RTC5, not from here."""

    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def configure(self) -> None:
        """External analog control and modulation on, hardware emission control off, guide off."""

    @abstractmethod
    def emission(self, on: bool) -> None: ...

    @abstractmethod
    def status(self) -> int:
        """The 32-bit STA word."""

    @abstractmethod
    def reset_errors(self) -> None: ...

    def guide(self, on: bool) -> None:
        pass

    def close(self) -> None:
        pass


class Axis(ABC):
    """One Zaber stage axis in mm (or its simulation)."""

    name: str = "axis"

    @abstractmethod
    def home(self, wait: bool = True) -> None: ...

    @abstractmethod
    def move_abs(self, pos_mm: float, speed: Optional[float] = None, accel: Optional[float] = None,
                 wait: bool = False) -> None: ...

    @abstractmethod
    def position(self) -> float: ...

    @abstractmethod
    def busy(self) -> bool: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def flags(self) -> Set[str]:
        """Zaber warning flags (two letters each; F* are faults)."""


class HeaterZone(ABC):
    """One stand-alone PID controller with its SSR (or its simulation)."""

    name: str = "zone"

    @abstractmethod
    def pv(self) -> float:
        """Process value in C; NaN if the thermocouple is open."""

    @abstractmethod
    def set_sv(self, celsius: float) -> None: ...

    @abstractmethod
    def run(self, on: bool) -> None: ...

    def output_pct(self) -> float:
        return float("nan")


class IoNode(ABC):
    """The Raspberry Pi 5 I/O node: relays, opto inputs, slow thermocouples and 4-20 mA inputs."""

    @abstractmethod
    def set(self, name: str, on: bool) -> None: ...

    @abstractmethod
    def get(self, name: str) -> bool: ...

    @abstractmethod
    def temps(self) -> Dict[str, float]: ...

    @abstractmethod
    def analog(self) -> Dict[str, float]: ...

    def snapshot(self) -> Dict[str, float]:
        """All inputs, temperatures and analog values in one request."""
        d = {k: self.get(k) for k in INPUTS}
        d.update(self.temps())
        d.update(self.analog())
        return d

    def heartbeat(self) -> None:
        pass


class Camera(ABC):
    @abstractmethod
    def capture(self, tag: str, layer: int) -> Optional[str]: ...


@dataclass
class Machine:
    scan: ScanCard
    laser: Laser
    piston: Axis
    recoater: Axis
    plate: HeaterZone
    block: HeaterZone
    io: IoNode
    camera: Optional[Camera] = None
    world: object = None        # the simulation, when there is one
