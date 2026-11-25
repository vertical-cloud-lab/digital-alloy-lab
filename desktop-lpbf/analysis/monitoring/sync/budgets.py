#!/usr/bin/env python3
"""Timing and data budgets for the in-situ monitoring (issue #260, monitoring/sync-and-data.md).

Numbers only, no model geometry. Every outside number has its source in SRC; numbers marked "assumed" are ours and say so.
Writes analysis/out/monitoring/sync/{timing_budget.md, data_budget.md, budgets.json}.

    python desktop-lpbf/analysis/monitoring/sync/budgets.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "out" / "monitoring" / "sync"
OUT.mkdir(parents=True, exist_ok=True)

SRC = {
    "rtc6": "SCANLAB RTC6 brochure (SCANLAB-RTC6-EN.pdf, 11/2026): 10 µs output period, laser signals at 15 ns resolution",
    "rtccmp": "SCANLAB RTC comparison table (SCANLAB-RTC-Comparison-EN.pdf): laser delays in 1/64 µs; 2 x 2^24 or 4 x 2^23 recorded values",
    "basicube": "SCANLAB basiCube 20 page (read 2026-11-25): tracking error 0.25 ms; step 0.58 ms (10 mrad); drift offset < 30 µrad/K, "
                "gain < 160 ppm/K; 8 h offset < 100 µrad, gain < 250 ppm; repeatability < 2 µrad RMS",
    "ipg": "electrical.md §11, from IPG's YLR-U3 sheet: on/off <= 12 µs, modulation <= 100 kHz",
    "pda": "Thorlabs PDA36A user guide table (via search): 260 kHz at 30 dB, 150 kHz at 40 dB, 45 kHz at 50 dB; the PDA36A2's own sheet not read",
    "pico": "PicoScope 4444 datasheet: 14-bit at 50 MS/s, streaming 10 MS/s (PicoScope 6) or 50 MS/s (SDK), timebase ±50 ppm, all channels "
            "sampled together, 3 ps RMS sample jitter, 1 MΩ || 17.5 pF per input",
    "gs": "Raspberry Pi documentation, Global Shutter Camera, external trigger: XTR is a 1.8 V input; exposure = low pulse + 14.26 µs; "
          "frame rate = pulse rate",
    "kron": "Kron Technologies, 'Triggering & Synchronizing Multiple Chronos Cameras' rev 0.1.0: with an external source, footage "
            "synchronised within 500 ns",
    "zel": "Zelenyak et al. 2015 (Sensors 15:11805), via edison/r8-ae-waveguide: each extra 76.5 mm of waveguide added ~15 µs",
    "nist": "Lane & Yeung 2020 (J. Res. NIST 125:125027): 100 kHz XYPT commands, 10 kHz coaxial camera, 20 µs exposure",
    "heat": "heat.md: 0.2 s of jumps per layer, 8 s recoat; dense L75 build +51 % time with the dwell (electrical.md §9.1)",
    "mon": "monitoring.md §5.3 and analysis/out/monitoring/optics.md (stream rates)",
}

SPEEDS = (0.4, 1.1)      # m/s: the process window's ends (monitoring.md, Edison queries)
TAU_US = 250.0            # basiCube 20 tracking error

# ------------------------------------------------------------------------------------------------- timing budget
# (path, element, fixed latency µs, uncertainty or jitter µs (±, 1 sigma-ish), basis, source key)
T = [
    ("beam position", "RTC6 output grid (the master clock)", 0.0, 0.0, "reference; outputs change only on 10 µs ticks", "rtc6"),
    ("beam position", "commanded -> actual spot (tracking delay), before calibration", TAU_US, 25.0, "±10 % assumed", "basicube"),
    ("beam position", "commanded -> actual spot, after the knife-edge test (§1.5)", TAU_US, 3.0, "assumed reach of the test", "basicube"),
    ("laser", "LASERON edge after mark start (LaserOnDelay)", 0.0, 0.016, "set in 1/64 µs steps; deterministic", "rtccmp"),
    ("laser", "gate -> light (IPG YLR-U3)", 12.0, 1.0, "<= 12 µs published; jitter assumed", "ipg"),
    ("photodiode", "PDA36A2 at 30 dB (260 kHz): group delay", 1e6 / (2 * math.pi * 260e3), 0.1, "first-order filter", "pda"),
    ("photodiode", "2.5 m RG-58", 2.5 * 5.1e-3, 0.0, "5.1 ns/m", "pda"),
    ("digitizer", "gate tap 10 kΩ into 17.5 pF: 50 % point of the RC step", 10e3 * 17.5e-12 * 1e6 * math.log(2), 0.02, "RC ln 2, calibrated out", "pico"),
    ("digitizer", "PicoScope at 2 MS/s: sample quantisation", 0.0, 0.5 / math.sqrt(12), "uniform over 0.5 µs", "pico"),
    ("digitizer", "clock vs RTC6, no fit, 30 s layer", 0.0, 100e-6 * 30e6, "±50 ppm each side (RTC6 assumed)", "pico"),
    ("digitizer", "clock vs RTC6, per-layer fit to gate edges", 0.0, 0.5, "bound; synthetic check gives less (reader_check.md)", "pico"),
    ("AE", "elastic path, plate and stack (10-25 mm at 5-6 km/s)", 3.0, 2.0, "assumed", "zel"),
    ("AE", "elastic path, 150-250 mm waveguide", 39.0, 10.0, "15 µs per 76.5 mm", "zel"),
    ("AE", "preamp and 50-600 kHz filter", 2.0, 1.0, "assumed", "zel"),
    ("coaxial camera", "trigger generator (RP2350 PIO, 150 MHz)", 0.05, 0.007, "one clock cycle; assumed", "gs"),
    ("coaxial camera", "XTR edge -> exposure start (IMX296)", 15.0, 15.0, "not published: assumed <= one line; measure (§1.5)", "gs"),
    ("coaxial camera", "frame time label = mid-exposure (50 µs exposure)", 25.0, 0.0, "by definition", "gs"),
    ("side camera", "Chronos exposure trigger on TRIG1 (BNC)", 0.0, 0.5, "within 500 ns", "kron"),
    ("layer camera", "software still after spread / after lasing", 1e5, 5e4, "assumed; the scene is static", "gs"),
    ("slow channels", "PLC -> Modbus TCP -> Pi timestamp", 2e4, 1e4, "assumed; module filtering not included", "heat"),
    ("Pi clock", "RTC6 layer-start bit on a Pi GPIO (kernel edge timestamp)", 50.0, 50.0, "assumed", "rtc6"),
]


def pos_um(t_us, v):
    return t_us * v                      # µs x m/s = µm


timing = [dict(path=p, element=e, latency_us=round(l, 3), uncertainty_us=round(u, 3), basis=b, source=s,
               **{f"pos_um_at_{v}": round(pos_um(u, v), 2) for v in SPEEDS}) for p, e, l, u, b, s in T]

# Mapping a photodiode sample to (x, y): what each correction is worth, at the two speeds.
cases = {
    "no clock fit, no tracking delay (DAQ started on a trigger, nominal rate; worst point of a 30 s layer)": math.hypot(TAU_US, 100e-6 * 30e6),
    "clock fit, tracking delay ignored": math.hypot(TAU_US, 0.5),
    "clock fit + tracking delay from the data sheet (±25 µs)": math.sqrt(25.0 ** 2 + 0.5 ** 2 + 0.1 ** 2 + 0.14 ** 2),
    "clock fit + tracking delay calibrated (±3 µs)": math.sqrt(3.0 ** 2 + 0.5 ** 2 + 0.1 ** 2 + 0.14 ** 2),
}
mapping = {k: {f"{v} m/s": round(pos_um(t, v), 1) for v in SPEEDS} | {"timing_us": round(t, 2)} for k, t in cases.items()}

# Static (non-timing) galvo errors at the edge of the L75 plate, f = 160 mm: these need the spot-grid calibration, not timing.
F_MM, R_MM = 160.0, 37.9
static = {
    "offset drift per K (30 µrad/K)": round(30e-6 * F_MM * 1e3, 1),
    "gain drift per K at r = 37.9 mm (160 ppm/K)": round(160e-6 * R_MM * 1e3, 1),
    "8 h offset drift (100 µrad)": round(100e-6 * F_MM * 1e3, 1),
    "8 h gain drift at r = 37.9 mm (250 ppm)": round(250e-6 * R_MM * 1e3, 1),
    "repeatability (2 µrad RMS)": round(2e-6 * F_MM * 1e3, 2),
}

# ------------------------------------------------------------------------------------------------- data budget
PLATES = {"S25": 25.2, "M50": 50.5, "L75": 75.8}
HATCH_MM, SPEED = 0.1, 1.0       # mm, m/s: area rate 100 mm^2/s (assumed mid-window)
RECOAT_S, JUMPS_S = 8.0, 0.2     # heat.md
BUILDS = [  # (name, plate, fraction scanned, height mm, dwell factor)
    ("B1: S25, 25 % scanned, 5 mm tall", "S25", 0.25, 5.0, 1.0),
    ("B2: M50, 25 % scanned, 10 mm tall", "M50", 0.25, 10.0, 1.0),
    ("B3: L75, 70 % scanned, 25 mm tall, with the dwell", "L75", 0.70, 25.0, 1.51),
]
LAYER_MM = 0.030
COOL_S = 3600.0                  # AE after the build (monitoring.md §4 step 4)

MB = 1e6
STREAMS = {  # bytes per second while running; "when": scan (lasing+jumps), build (whole build), cool (cool-down), layer (per layer, bytes)
    "RTC6 command log, 100 kHz x 12 B (x, y int32; power, gate+outputs uint16)": (100e3 * 12, "scan"),
    "PicoScope 4 ch x 2 MS/s x 16-bit, raw": (4 * 2e6 * 2, "scan"),
    "photodiodes kept at 200 kS/s x 2 ch (decimated from 2 MS/s)": (2 * 200e3 * 2, "scan"),
    "AE raw 2 MS/s x 16-bit": (2e6 * 2, "scan"),
    "coaxial IMX296 128 x 96 at 536 fps, 16-bit unpacked": (128 * 96 * 2 * 536, "scan"),
    "NIST-class coaxial camera 120 x 120 x 8-bit at 10 kHz": (120 * 120 * 10e3, "scan"),
    "layer camera video H.264 ~15 Mbit/s": (15e6 / 8, "build"),
    "layer stills: 4 x 18.5 MB (12-bit raw) per layer": (4 * 4056 * 3040 * 1.5, "layer"),
    "PLC slow channels, 20 x 8 B at 10 Hz": (20 * 8 * 10, "build"),
    "AE hits only (~100 hits/h x 4 ms snippets at 2 MS/s)": (100 / 3600 * 8000 * 2, "build+cool"),
    "Chronos 2.1-HD burst, 32 GB (15.5 s at 640 x 96, 24 kfps)": (32e9, "burst"),
}
CONFIGS = {
    "baseline (monitoring.md §4 steps 1-6)": [
        "RTC6 command log, 100 kHz x 12 B (x, y int32; power, gate+outputs uint16)",
        "photodiodes kept at 200 kS/s x 2 ch (decimated from 2 MS/s)", "AE raw 2 MS/s x 16-bit",
        "AE hits only (~100 hits/h x 4 ms snippets at 2 MS/s)",
        "coaxial IMX296 128 x 96 at 536 fps, 16-bit unpacked", "layer camera video H.264 ~15 Mbit/s",
        "layer stills: 4 x 18.5 MB (12-bit raw) per layer", "PLC slow channels, 20 x 8 B at 10 Hz"],
    "everything raw (4 ch continuous from build start to 1 h after, 4 Chronos bursts)": [
        "RTC6 command log, 100 kHz x 12 B (x, y int32; power, gate+outputs uint16)",
        "PicoScope 4 ch x 2 MS/s x 16-bit, raw [continuous]",
        "coaxial IMX296 128 x 96 at 536 fps, 16-bit unpacked", "layer camera video H.264 ~15 Mbit/s",
        "layer stills: 4 x 18.5 MB (12-bit raw) per layer", "PLC slow channels, 20 x 8 B at 10 Hz",
        "Chronos 2.1-HD burst, 32 GB (15.5 s at 640 x 96, 24 kfps) [x4]"],
}


def build_times(plate, frac, height, dwell):
    area = frac * math.pi * (PLATES[plate] / 2) ** 2
    lasing = area / (HATCH_MM * SPEED * 1e3)            # s per layer
    scan = lasing * 1.10 + JUMPS_S                       # +10 % for mark/jump delays (assumed)
    layer = (scan + RECOAT_S) * dwell
    n = round(height / LAYER_MM)
    return dict(area_mm2=round(area, 1), lasing_s_per_layer=round(lasing, 2), scan_s_per_layer=round(scan, 2),
                layer_s=round(layer, 1), layers=n, build_h=round(n * layer / 3600, 2), lasing_h=round(n * lasing / 3600, 2),
                scan_h=round(n * scan / 3600, 2))


def stream_bytes(name, bt):
    key = name.replace(" [continuous]", "").replace(" [x4]", "")
    rate, when = STREAMS[key]
    if name.endswith("[continuous]"):
        return rate * (bt["build_h"] * 3600 + COOL_S)
    if name.endswith("[x4]"):
        return rate * 4
    if when == "scan":
        return rate * bt["scan_h"] * 3600
    if when == "build":
        return rate * bt["build_h"] * 3600
    if when == "build+cool":
        return rate * (bt["build_h"] * 3600 + COOL_S)
    if when == "layer":
        return rate * bt["layers"]
    raise ValueError(name)


builds = []
for name, plate, frac, h, dwell in BUILDS:
    bt = build_times(plate, frac, h, dwell)
    per = {cfg: {s: round(stream_bytes(s, bt) / 1e9, 2) for s in lst} for cfg, lst in CONFIGS.items()}
    tot = {cfg: round(sum(v.values()), 1) for cfg, v in per.items()}
    # Pi share per layer (coaxial camera during the scan + 4 stills) and the time to move it over GbE during the recoat
    pi_layer_MB = (STREAMS["coaxial IMX296 128 x 96 at 536 fps, 16-bit unpacked"][0] * bt["scan_s_per_layer"]
                   + STREAMS["layer stills: 4 x 18.5 MB (12-bit raw) per layer"][0]) / MB
    builds.append(dict(name=name, **bt, per_stream_GB=per, total_GB=tot, pi_MB_per_layer=round(pi_layer_MB, 0),
                       pi_to_pc_s_at_110MBps=round(pi_layer_MB / 110, 1)))

# Host capacities (what each computer has to carry), with sources in sync-and-data.md §3.2
HOSTS = {
    "Pi 5: coaxial camera + layer video while scanning (MB/s)": round((STREAMS["coaxial IMX296 128 x 96 at 536 fps, 16-bit unpacked"][0]
                                                                  + STREAMS["layer camera video H.264 ~15 Mbit/s"][0]) / MB, 1),
    "Pi 5: PCIe Gen 2 x1 to the NVMe, ceiling (MB/s, Raspberry Pi: ~500)": 500,
    "Pi 5: Gigabit Ethernet, practical (MB/s, assumed)": 110,
    "scan PC: PicoScope 4 ch x 2 MS/s (MB/s)": round(STREAMS["PicoScope 4 ch x 2 MS/s x 16-bit, raw"][0] / MB, 1),
    "scan PC: PicoScope SDK streaming ceiling (MS/s, all channels)": 50,
    "scan PC: RTC6 log (MB/s)": round(STREAMS["RTC6 command log, 100 kHz x 12 B (x, y int32; power, gate+outputs uint16)"][0] / MB, 1),
    "NIST-class coaxial camera (MB/s): needs a frame grabber in the PC, not the Pi": round(STREAMS["NIST-class coaxial camera 120 x 120 x 8-bit at 10 kHz"][0] / MB, 0),
    "Chronos 32 GB burst over GbE at 110 MB/s (min)": round(32e3 / 110 / 60, 1),
}

R = dict(sources=SRC, timing=timing, mapping_error_um=mapping, static_galvo_um=static, builds=builds, hosts=HOSTS,
         assumptions=dict(hatch_mm=HATCH_MM, speed_m_s=SPEED, recoat_s=RECOAT_S, jumps_s=JUMPS_S, layer_mm=LAYER_MM,
                          scan_overhead="+10 % of lasing for mark and jump delays", cool_down_s=COOL_S))
(OUT / "budgets.json").write_text(json.dumps(R, indent=1, ensure_ascii=False))

# ------------------------------------------------------------------------------------------------- markdown
L = ["# Timing budget (generated by analysis/monitoring/sync/budgets.py)", "",
     "Latency is a fixed delay that calibration removes; uncertainty is what is left (or the jitter). Position = uncertainty x speed.", "",
     "| path | element | latency (µs) | uncertainty (µs) | at 0.4 m/s (µm) | at 1.1 m/s (µm) | basis | source |",
     "|---|---|---:|---:|---:|---:|---|---|"]
for r in timing:
    L.append(f"| {r['path']} | {r['element']} | {r['latency_us']:g} | {r['uncertainty_us']:g} | {r['pos_um_at_0.4']:g} | "
             f"{r['pos_um_at_1.1']:g} | {r['basis']} | {r['source']} |")
L += ["", "## Mapping a photodiode sample to (x, y)", "", "| correction applied | timing error (µs) | at 0.4 m/s (µm) | at 1.1 m/s (µm) |",
      "|---|---:|---:|---:|"]
for k, v in mapping.items():
    L.append(f"| {k} | {v['timing_us']:g} | {v['0.4 m/s']:g} | {v['1.1 m/s']:g} |")
L += ["", "## Static galvo errors (need the spot-grid calibration, not timing)", "", "| item | µm |", "|---|---:|"]
L += [f"| {k} | {v:g} |" for k, v in static.items()]
L += ["", "## Sources", ""] + [f"- **{k}**: {v}" for k, v in SRC.items()]
(OUT / "timing_budget.md").write_text("\n".join(L) + "\n")

D = ["# Data budget per build (generated by analysis/monitoring/sync/budgets.py)", "",
     f"Assumed: {HATCH_MM} mm hatch at {SPEED} m/s (100 mm²/s), {LAYER_MM * 1e3:.0f} µm layers, {JUMPS_S} s of jumps and an "
     f"{RECOAT_S:.0f} s recoat per layer (heat.md), +10 % of lasing for delays, AE kept for {COOL_S / 3600:.0f} h after the build.", "",
     "| build | layers | lasing per layer (s) | layer (s) | build (h) | lasing (h) |", "|---|---:|---:|---:|---:|---:|"]
for b in builds:
    D.append(f"| {b['name']} | {b['layers']} | {b['lasing_s_per_layer']} | {b['layer_s']} | {b['build_h']} | {b['lasing_h']} |")
for cfg in CONFIGS:
    D += ["", f"### {cfg}: GB per build", "", "| stream | " + " | ".join(b["name"].split(":")[0] for b in builds) + " |",
          "|---|" + "---:|" * len(builds)]
    for s in CONFIGS[cfg]:
        D.append(f"| {s} | " + " | ".join(f"{b['per_stream_GB'][cfg][s]:g}" for b in builds) + " |")
    D.append("| **total** | " + " | ".join(f"**{b['total_GB'][cfg]:g}**" for b in builds) + " |")
D += ["", "### The Pi's share per layer, and moving it to the scan PC during the recoat", "",
      "| build | Pi data per layer (MB): coaxial camera + 4 stills | over GbE at 110 MB/s (s) | recoat (s) |", "|---|---:|---:|---:|"]
D += [f"| {b['name']} | {b['pi_MB_per_layer']:g} | {b['pi_to_pc_s_at_110MBps']:g} | {RECOAT_S:g} |" for b in builds]
D += ["", "### What each computer carries", "", "| item | value |", "|---|---:|"] + [f"| {k} | {v:g} |" for k, v in HOSTS.items()]
(OUT / "data_budget.md").write_text("\n".join(D) + "\n")
print("\n".join(L[:3]))
print(json.dumps({b["name"]: b["total_GB"] for b in builds}, indent=1))
print(json.dumps(mapping, indent=1))
