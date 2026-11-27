"""ftctl: build supervisor for the FT-1 purge-box LPBF (desktop-lpbf/fast-track, issue #260).

The supervisor runs the layer loop (interlocks and O2 -> recoat -> plate step -> scan -> log -> dwell) on top of small
hardware interfaces (ftctl.hw.interfaces). Every device has a simulated backend (ftctl.hw.sim) so a whole build runs on
a laptop or CI runner; the real backends are ftctl.hw.rtc5 (SCANLAB RTC5 DLL via ctypes), ftctl.hw.ipg (IPG YLR over
RS-232), ftctl.hw.zaber (zaber-motion), ftctl.hw.pinode (Raspberry Pi 5 I/O node: gpiozero relays and inputs, MCC
DAQ HATs, Modbus PID controllers).

Safety is hard-wired (Omron G9SE-201, lid and beam-tube switches, E-stop, key, temperature switches, CN708 heater
limit). Nothing in this package can close the laser's interlock loop; software only requests emission and can always
stop it (ftctl.interlock models the hard-wired chain and checks it).
"""

__version__ = "0.1.0"
