"""One time base for the whole build.

Every record the supervisor writes is stamped with Clock.now(): seconds since the clock was started, from the PC's
monotonic clock (RealClock) or from the simulation (SimClock). Other devices are tied to it, not to their own clocks:
- the RTC5 raises DIGITAL OUT1 (LASER connector pin 12) for the length of every layer's list, and the recorder that
  samples the photodiode and AE sensor records that pin and LASERON (pin 2) on its own sample clock, so each fast
  sample maps onto the layer and onto the RTC5's set_trigger4 trace (which shares LASERON);
- the Raspberry Pi's slow channels are read by request and stamped on the PC when the reply arrives (< 10 ms on a
  direct Ethernet link), which is far below their 1 s logging period.
"""
from __future__ import annotations

import time
from typing import Callable, List


class Clock:
    def now(self) -> float:
        raise NotImplementedError

    def sleep(self, dt: float) -> None:
        raise NotImplementedError


class RealClock(Clock):
    def __init__(self):
        self._t0 = time.monotonic()
        self.wall_t0 = time.time()

    def now(self) -> float:
        return time.monotonic() - self._t0

    def sleep(self, dt: float) -> None:
        if dt > 0:
            time.sleep(dt)


class SimClock(Clock):
    """Simulated time. sleep(dt) advances the simulated world by dt. speed = 0 runs as fast as the CPU allows;
    speed = N paces the simulation at N x real time (for watching it)."""

    def __init__(self, speed: float = 0.0, max_step: float = 0.25):
        self.t = 0.0
        self.speed = speed
        self.max_step = max_step
        self.wall_t0 = time.time()
        self._listeners: List[Callable[[float, float], None]] = []

    def on_advance(self, fn: Callable[[float, float], None]) -> None:
        self._listeners.append(fn)

    def now(self) -> float:
        return self.t

    def sleep(self, dt: float) -> None:
        while dt > 1e-12:
            h = min(dt, self.max_step)
            t0, t1 = self.t, self.t + h
            for fn in self._listeners:
                fn(t0, t1)
            self.t = t1
            dt -= h
            if self.speed > 0:
                time.sleep(h / self.speed)
