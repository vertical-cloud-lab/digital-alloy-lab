#!/usr/bin/env python3
"""A synthetic three-layer build written in the lpbf_h5 layout, and a check of the reader against the truth (issue #260,
monitoring/sync-and-data.md §4).

What is simulated (all assumptions, chosen to be plausible, not measured):
- the RTC6: three 2 x 2 mm squares per layer on an S25 plate, serpentine hatch at 1 m/s, 0.1 mm hatch, x and y alternating;
  jumps at 3 m/s; LaserOnDelay 150 µs, LaserOffDelay 250 µs, mark delay 300 µs, jump delay 250 µs; logged every 10 µs;
- the scan head: a critically damped second-order follower whose lag at constant speed is 250 µs (the basiCube 20's
  tracking error). The reader is NOT given this model: it uses either a pure 250 µs delay or a first-order lag;
- the digitizer: 500 kS/s here (2 MS/s in the design; smaller file), started 1.23 ms before each layer, its crystal 73 ppm fast;
- the photodiodes: brighter where the spot moves slowly (track starts) and a hot spot (r ~ 0.1 mm) planted in layer 2;
- the coaxial camera: one trigger 300 µs after each track starts (536 fps is longer than a 2 mm track), exposure 50 µs,
  trigger-to-exposure 6 µs + up to 14.3 µs of jitter; one frame dropped in layer 3.

Writes analysis/out/monitoring/sync/{synthetic_build.h5, synthetic_tree.md, reader_check.md, reader_check.json, reader_check.png}.

    python desktop-lpbf/analysis/monitoring/sync/synthetic_build.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import h5py
import numpy as np
from scipy.signal import cont2discrete, lfilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lpbf_h5 as lh  # noqa: E402

OUT = lh.OUT
RNG = np.random.default_rng(260)

# ------------------------------------------------------------------------------------------------ truth and settings
TICK = 10.0                         # µs
DT = 0.5                            # µs, fine grid for the physics
TAU_SS = 250.0                      # µs, scan head lag at constant speed (truth)
W = 2.0 / TAU_SS                    # rad/µs: critically damped, lag 2/w
P = dict(id=1, name="AlSi10Mg screen", power_W=300.0, speed_mm_s=1000.0, jump_speed_mm_s=3000.0, hatch_um=100.0, layer_um=30.0,
         laser_on_delay_us=150.0, laser_off_delay_us=250.0, mark_delay_us=300.0, jump_delay_us=250.0, polygon_delay_us=100.0,
         skywriting=0, strategy="serpentine, x/y alternating")
PARTS = [(1, "cube A", -4.0, -2.0), (2, "cube B", 3.0, -2.0), (3, "cube C", 0.0, 4.0)]
SIDE = 2.0                          # mm
DEFECT = dict(layer=2, x=-4.25, y=-1.62, r=0.12, gain=1.0)        # planted hot spot (Gaussian sigma r, +100 %): spans 3 tracks
FS = 500e3                          # DAQ, Hz (nominal)
DRIFT = 73e-6                       # DAQ crystal fast by 73 ppm
DAQ_LEAD = 1234.567                 # µs, DAQ segment starts this long before the layer t0
LASER_DELAY, LASER_TAU = 2.0, 3.0   # µs, gate -> light (truth)
PD_TAU = 1e6 / (2 * np.pi * 260e3)  # PDA36A2 at 30 dB
TAP_TAU = 10e3 * 17.5e-12 * 1e6     # gate tap RC, µs
CAM = dict(period=1e6 / 536, delay=300.0, exposure=50.0, lat=6.0, jitter=14.3, h=24, w=32, spot=(15.2, 11.6))
CAL = dict(tracking_delay_us=250.0, tracking_delay_unc_us=3.0, galvo_model="lag1", laser_rise_us=4.0, pd_delay_us=0.6,
           gate_tap_delay_us=0.12, ae_path_delay_us=40.0, coax_trigger_to_exposure_us=13.2, coax_trigger_jitter_us=4.1,
           chronos_trigger_to_exposure_us=0.3, gen_latency_us=0.05, method="synthetic: the values the simulation used, rounded",
           date_utc="2026-11-25T00:00:00Z")
VPC = 10.0 / 65536                  # ±5 V range, 16-bit counts
T0_TICK0 = 4_200_000_000            # RTC6 tick at the first layer (arbitrary)
T0_UTC_NS = int(np.datetime64("2026-11-25T08:00:00", "ns").astype(np.int64))


def hatch(layer):
    """Track list: (part, x0, y0, x1, y1) in plate mm, serpentine, x hatch on odd layers and y hatch on even ones."""
    out = []
    n = int(round(SIDE / (P["hatch_um"] * 1e-3)))
    for pid, _, cx, cy in PARTS:
        for i in range(n):
            o = -SIDE / 2 + (i + 0.5) * SIDE / n
            a, b = (-SIDE / 2, SIDE / 2) if i % 2 == 0 else (SIDE / 2, -SIDE / 2)
            out.append((pid, cx + a, cy + o, cx + b, cy + o) if layer % 2 else (pid, cx + o, cy + a, cx + o, cy + b))
    return out


def command(layer):
    """The RTC6's 10 µs output for one layer, the track table and the exact gate edges (µs after t0)."""
    xs, ys, dout = [0.0] * 50, [0.0] * 50, [2] * 10 + [0] * 40       # 0.5 ms hold at the start; bit 1 = layer start
    tracks, toggle = [], 0
    for k, (pid, x0, y0, x1, y1) in enumerate(hatch(layer)):
        cx, cy = xs[-1], ys[-1]
        nj = max(1, int(np.ceil(np.hypot(x0 - cx, y0 - cy) / (P["jump_speed_mm_s"] * TICK * 1e-6))))
        for i in range(1, nj + 1):
            xs.append(cx + (x0 - cx) * i / nj); ys.append(cy + (y0 - cy) * i / nj); dout.append(toggle)
        for _ in range(int(P["jump_delay_us"] / TICK)):
            xs.append(x0); ys.append(y0); dout.append(toggle)
        toggle ^= 4                                                   # bit 2 toggles at each mark start
        t_start = len(xs) * TICK
        nm = int(round(np.hypot(x1 - x0, y1 - y0) / (P["speed_mm_s"] * TICK * 1e-6)))
        for i in range(1, nm + 1):
            xs.append(x0 + (x1 - x0) * i / nm); ys.append(y0 + (y1 - y0) * i / nm); dout.append(toggle | 1)   # bit 0 = window
        t_end = len(xs) * TICK
        for _ in range(int(P["mark_delay_us"] / TICK)):
            xs.append(x1); ys.append(y1); dout.append(toggle)
        tracks.append(dict(track=k, part=pid, kind=0, param_set=1, t_start_us=t_start, t_end_us=t_end, x0_mm=x0, y0_mm=y0,
                           x1_mm=x1, y1_mm=y1, speed_mm_s=P["speed_mm_s"], power_W=P["power_W"], camera=1))
    for _ in range(50):
        xs.append(xs[-1]); ys.append(ys[-1]); dout.append(toggle)
    x, y, dout = np.array(xs, np.float64), np.array(ys, np.float64), np.array(dout, np.uint16)
    on = np.array([t["t_start_us"] + P["laser_on_delay_us"] for t in tracks])
    off = np.array([t["t_end_us"] + P["laser_off_delay_us"] for t in tracks])
    tt = np.arange(len(x)) * TICK
    k = np.searchsorted(on, tt, side="right") - 1
    laser = ((k >= 0) & (tt < off[np.clip(k, 0, None)])).astype(np.uint8)
    return x, y, dout, laser, tracks, on, off


def follower(u_fine):
    """Critically damped second-order scan-head model, unit DC gain, on the fine grid."""
    b, a, _ = cont2discrete(([W * W], [1.0, 2 * W, W * W]), DT, method="zoh")
    return lfilter(b.ravel(), a, u_fine - u_fine[0]) + u_fine[0]


def first_order(sig, tau):
    k = np.exp(-DT / tau)
    return lfilter([1 - k], [1, -k], sig, zi=[k * sig[0]])[0]


def simulate(layer):
    x, y, dout, laser, tracks, on, off = command(layer)
    n = len(x)
    tf = np.arange(0.0, n * TICK, DT)
    i = np.minimum((tf // TICK).astype(int), n - 1)
    xa, ya = follower(x[i]), follower(y[i])                         # true beam position
    gate = np.zeros_like(tf)
    for a_, b_ in zip(on, off):
        gate[(tf >= a_) & (tf < b_)] = 1.0
    light = first_order(np.interp(tf - LASER_DELAY, tf, gate, left=0.0), LASER_TAU)
    v = np.hypot(np.gradient(xa, DT), np.gradient(ya, DT)) * 1e6 / P["speed_mm_s"]   # relative speed
    slow = 1.0 + 0.8 * np.clip(1.0 - v, 0.0, 1.0)
    hot = 1.0 + (DEFECT["gain"] * np.exp(-((xa - DEFECT["x"]) ** 2 + (ya - DEFECT["y"]) ** 2) / (2 * DEFECT["r"] ** 2))
                 if layer == DEFECT["layer"] else 0.0)
    pd1 = first_order(2.0 * light * slow * hot + 0.02, PD_TAU)
    pd2 = first_order(1.1 * light * slow * hot * (1 + 0.15 * (hot - 1)) + 0.02, PD_TAU)
    # DAQ: sample k at RTC time t0 - lead + k / (fs (1 + drift))
    ts = -DAQ_LEAD + np.arange(int((n * TICK + DAQ_LEAD + 1000) * FS * 1e-6)) / (FS * (1 + DRIFT)) * 1e6
    ts = ts[ts < tf[-1]]
    # gate tap: exact RC response at the sample times (the 0.5 µs grid is too coarse for a 0.18 µs RC)
    e_t = np.r_[on, off]
    e_v = np.r_[np.ones(len(on)), np.zeros(len(off))]
    o = np.argsort(e_t)
    e_t, e_v = e_t[o], e_v[o]
    j = np.searchsorted(e_t, ts, side="right") - 1
    before = np.where(j >= 1, e_v[np.clip(j - 1, 0, None)], 0.0)
    after = np.where(j >= 0, e_v[np.clip(j, 0, None)], 0.0)
    since_e = np.where(j >= 0, ts - e_t[np.clip(j, 0, None)], 1e9)
    gtap_s = 5.0 * (before + (after - before) * (1 - np.exp(-since_e / TAP_TAU)))
    ae = RNG.normal(0, 0.005, ts.size)
    burst_t = RNG.choice(ts[np.interp(ts, tf, gate) > 0.5], size=6, replace=False)
    for bt in burst_t:                                            # process bursts while lasing
        m = ts >= bt
        ae[m] += 0.04 * RNG.uniform(0.5, 1.5) * np.exp(-(ts[m] - bt) / 300.0) * np.sin(2 * np.pi * 0.15 * (ts[m] - bt))
    chans = dict(pd1=np.interp(ts, tf, pd1) + RNG.normal(0, 0.01, ts.size), pd2=np.interp(ts, tf, pd2) + RNG.normal(0, 0.008, ts.size),
                 ae=ae, gate=gtap_s + RNG.normal(0, 0.002, ts.size))
    daq = {c: np.clip(np.round(v_ / VPC), -32768, 32767).astype(np.int16) for c, v_ in chans.items()}
    truth = dict(tf=tf, xa=xa, ya=ya, ts=ts, burst_t=burst_t, hot=hot, pd1=pd1)
    return x, y, dout, laser, tracks, on, off, daq, truth


def camera(tracks, truth, layer, drop=None):
    """One frame per trigger; brightness from the true photodiode over the exposure; returns arrays for coax_cam."""
    tf, pd1 = truth["tf"], truth["pd1"]
    trig = []
    for t in tracks:
        tt = t["t_start_us"] + CAL["gen_latency_us"] + CAM["delay"]
        while tt + CAM["exposure"] < t["t_end_us"]:
            trig.append((tt, t["track"]))
            tt += CAM["period"]
    frames, rows = [], []
    yy, xx = np.mgrid[0:CAM["h"], 0:CAM["w"]]
    for j, (tt, tr) in enumerate(trig):
        if drop is not None and j == drop:
            continue
        t_exp = tt + CAM["lat"] + RNG.uniform(0, CAM["jitter"])
        m = (tf >= t_exp) & (tf < t_exp + CAM["exposure"])
        b = float(pd1[m].mean()) if m.any() else 0.0
        img = 1200 * b * np.exp(-((xx - CAM["spot"][0]) ** 2 / 18.0 + (yy - CAM["spot"][1]) ** 2 / 8.0)) + RNG.normal(40, 4, xx.shape)
        frames.append(np.clip(img, 0, 4095).astype(np.uint16))
        rows.append((j, tt + CAL["coax_trigger_to_exposure_us"] + CAM["exposure"] / 2, tr,
                     int(T0_UTC_NS + (t_exp + CAM["exposure"] + 900.0 + RNG.uniform(0, 200.0)) * 1e3)))
    return np.array(frames), rows


def write():
    path = OUT / "synthetic_build.h5"
    f = lh.create(path, build_id="synthetic-20261125-s25", writer="synthetic_build.py", layer_template=False)
    f["/build"].attrs.update(start_utc="2026-11-25T08:00:00Z", run_by="synthetic", recipe="screen-AlSi10Mg-300W",
                             scan_file="synthetic.job", alloy="AlSi10Mg", powder_lot="SYN-0001", plate_id="S25-SYN-01",
                             plate_material="6061-T6", module="S25", module_id="S25-1", layer_um=30.0, n_layers=3,
                             plate_setpoint_C=200.0, focus_offset_mm=0.0, spot_um=96.0, field_correction="synthetic.ct5",
                             cover_slide_count=1, start_O2_ppm=180.0, start_dewpoint_C=-52.0, power_check_W=301.5,
                             software_commit="0000000", rtc6_software="synthetic",
                             monitoring_config=json.dumps(dict(daq_fs_Hz=FS, pd_gain_dB=30, coax_fps=536, coax_exposure_us=CAM["exposure"])))
    lh.append(f["/build/parts"], [dict(part=p, name=nm, x_mm=x, y_mm=y, rot_deg=0.0, param_set=1, stl_sha256="") for p, nm, x, y in PARTS])
    lh.append(f["/build/param_sets"], [P])
    f["/calibration/timing"].attrs.update(CAL)
    f["/calibration/geometry"].attrs.update(rtc_bits_per_mm=2 ** 20 / 60.0, coax_um_per_px=8.0, coax_spot_px=list(CAM["spot"]),
                                            coax_rotation_deg=0.0, plate_from_rtc=np.eye(2, 3), layer_cam_homography=np.eye(3),
                                            side_cam_homography=np.eye(3), date_utc=CAL["date_utc"])
    f["/calibration/radiometry"].attrs.update(pd1_band_nm=[700.0, 25.0], pd2_band_nm=[950.0, 25.0], pd1_gain_dB=30.0, pd2_gain_dB=30.0,
                                              pd1_dark_V=0.02, pd2_dark_V=0.02, lamp="none (synthetic)")
    f["/calibration/ae"].attrs.update(sensor="synthetic broadband", preamp="40 dB", gain_dB=40.0, filter_kHz=[50.0, 600.0],
                                      threshold_dBAE=45.0, couplant="none", preload_N=15.0)
    lh.append(f["/calibration/ae/plb"], [dict(x_mm=x, y_mm=y, amplitude_dBAE=97.0 + RNG.normal(0, 1.5), t_utc_ns=T0_UTC_NS - 600_000_000_000)
                                         for x, y in [(-8, 0), (8, 0), (0, 8), (0, -8), (0, 0)]])
    truths, t_utc = {}, T0_UTC_NS
    tick = T0_TICK0
    for layer in (1, 2, 3):
        x, y, dout, laser, tracks, on, off, daq, truth = simulate(layer)
        truths[layer] = (truth, tracks, on, off)
        g = lh.add_layer(f, layer)
        n_us = len(x) * TICK
        g.attrs.update(layer=layer, z_mm=layer * 0.03, t0_tick=np.uint64(tick), t0_pi_ns=np.uint64(t_utc + 37_000),
                       t0_utc=str(np.datetime64(t_utc, "ns"))[:23] + "Z", scan_end_us=float(tracks[-1]["t_end_us"]),
                       dwell_s=0.0, plate_T_start_C=200.0 + layer * 0.4, n_tracks=len(tracks), hatch_angle_deg=0.0 if layer % 2 else 90.0)
        r = g["rtc"]
        r.attrs.update(period_us=TICK, source="synthetic (RTC6 set_trigger4 would log SampleX, SampleY, LaserOn, output port)",
                       signals="SampleX, SampleY, LaserOn, digital output")
        lh.put(r["x_mm"], x, units="mm"); lh.put(r["y_mm"], y); lh.put(r["power_W"], laser * P["power_W"])
        lh.put(r["laser_on"], laser); lh.put(r["dout"], dout)
        lh.append(g["tracks"], tracks)
        d = g["daq"]
        d.attrs.update(fs_Hz=FS, t0_index=0, clock_a_us=np.nan, clock_b=np.nan, clock_fit_rms_us=np.nan, clock_fit_edges=0,
                       instrument="synthetic PicoScope 4444, 14-bit, ±5 V")
        for c, v in daq.items():
            lh.put(d[c], v, volts_per_count=VPC, offset_V=0.0, range_V=5.0)
        # AE hits: the process bursts the threshold finds, and (layer 2) a crack-like hit 1.7 s after the scan, in the recoat
        hits, snips = [], []
        for bt in truth["burst_t"]:
            hits.append(dict(t_us=bt - CAL["ae_path_delay_us"], peak_V=0.04, amplitude_dBAE=72.0, energy_V2s=1e-7, rise_us=5.0,
                             duration_us=900.0, counts=40, rms_V=0.01, skewness=0.0, kurtosis=3.0, snippet=-1, label=0))
        if layer == DEFECT["layer"]:
            ts = np.arange(4000) / 2e6 * 1e6
            s = 0.9 * np.exp(-ts / 700.0) * np.sin(2 * np.pi * 0.1 * ts) * (ts > 200) + RNG.normal(0, 0.005, ts.size)
            snips.append(np.round(s / VPC).astype(np.int16))
            hits.append(dict(t_us=n_us + 1.7e6, peak_V=0.9, amplitude_dBAE=99.0, energy_V2s=2.1e-4, rise_us=3.0, duration_us=2400.0,
                             counts=310, rms_V=0.21, skewness=0.05, kurtosis=4.1, snippet=0, label=1))
        lh.append(g["ae_hits"], hits)
        lh.put(g["ae_snippets"], np.array(snips).reshape(len(snips), 4000) if snips else np.zeros((0, 4000), np.int16),
               fs_Hz=2e6, pre_samples=400, volts_per_count=VPC)
        frames, rows = camera(tracks, truth, layer, drop=17 if layer == 3 else None)
        c = g["coax_cam"]
        c.attrs.update(sensor="IMX296 mono (synthetic)", roi=[0, 0, CAM["w"], CAM["h"]], band_nm=[950.0, 10.0], analogue_gain=4.0,
                       trigger_period_us=CAM["period"], trigger_delay_us=CAM["delay"])
        lh.put(c["frames"], frames)
        lh.put(c["trigger_index"], [r_[0] for r_ in rows]); lh.put(c["t_mid_us"], [r_[1] for r_ in rows])
        lh.put(c["track"], [r_[2] for r_ in rows]); lh.put(c["pi_ts_ns"], [r_[3] for r_ in rows])
        lh.put(c["exposure_us"], np.full(len(rows), CAM["exposure"]))
        yy, xx = np.mgrid[0:48, 0:64]
        li = g["layer_images"]
        for stage in ("after_spread", "after_lasing"):
            img = 600 + 30 * xx / 64 + RNG.normal(0, 8, xx.shape)
            if stage == "after_lasing":
                for _, _, cx, cy in PARTS:
                    img[(np.abs(xx - 32 - cx * 2.5) < 2.5) & (np.abs(yy - 24 + cy * 2.5) < 2.5)] += 900
            nm = f"{stage}_raking"
            ds = li[nm] if nm in li else li.create_dataset(nm, shape=(0, 0), maxshape=(None, None), dtype="u2", chunks=True,
                                                             compression="gzip", compression_opts=4, shuffle=True, fletcher32=True)
            lh.put(ds, np.clip(img, 0, 4095), units="DN")
            ds.attrs.update(stage=stage, light="raking (back-wall window)", exposure_us=8000.0, analogue_gain=1.0, sensor_temp_C=41.0,
                            t_utc=str(np.datetime64(t_utc + int((n_us + (2e6 if stage == "after_lasing" else -6e6)) * 1e3), "ns"))[:23] + "Z")
        layer_s = n_us * 1e-6 + 8.0
        tick += int(layer_s * 1e5)
        t_utc += int(layer_s * 1e9)
    # slow channels at 2 Hz and AE in the cool-down
    t = np.arange(T0_UTC_NS - 10_000_000_000, t_utc + 60_000_000_000, 500_000_000)
    lay = np.clip(np.searchsorted([T0_UTC_NS + i * int((0.17 + 8) * 1e9) for i in range(3)], t, side="right"), 0, 3)
    lh.append(f["/slow"], [dict(t_utc_ns=int(tt), layer=int(l_), plate_T_C=200 + RNG.normal(0, 0.2), edge_T_C=197 + RNG.normal(0, 0.2),
                                wall_T_C=31.0, cake_T_C=24.0, heater_duty=0.41, O2_ppm=180 - 10 * l_, dewpoint_C=-52.0, p_abs_mbar=1023.0,
                                dp_mbar=12.0, pirani_mbar=np.nan, blower_pct=60.0, recoater_mm=0.0, recoater_torque_pct=3.0,
                                z_mm=0.03 * l_, door_closed=1, drawer_closed=1, laser_ready=1, emission_on=1) for tt, l_ in zip(t, lay)])
    lh.append(f["/ae_cooldown"], [dict(t_utc_ns=t_utc + m * 60_000_000_000, peak_V=pk, amplitude_dBAE=dB, energy_V2s=e, plate_T_C=Tp, label=lb)
                                  for m, pk, dB, e, Tp, lb in [(5, 0.05, 74, 2e-7, 160, 0), (12, 0.7, 97, 1.5e-4, 121, 1), (41, 0.06, 75, 2e-7, 58, 0)]])
    f["/build"].attrs["end_utc"] = str(np.datetime64(t_utc, "ns"))[:23] + "Z"
    f.close()
    return path, truths


def postprocess(path, truths):
    """What the scan PC does after each layer: fit the clock, label frames with x, y, fill per-track features, flag events."""
    B = lh.Build(path)
    fits, feats, events = {}, {}, []
    for L in B.layers():
        a, b = B.clock(L, refit=True)
        g = B.f[f"/layers/{L}"]
        tr, ps = g["tracks"][...], B.f["/build/param_sets"][...]
        eon, eoff = lh.gate_edges_expected(tr, ps)
        son, soff = lh.gate_edges_seen(g["daq/gate"][...], g["daq"].attrs["fs_Hz"])
        _, _, rms, ne = lh.fit_clock(son, soff, eon, eoff, tap_us=CAL["gate_tap_delay_us"])
        fits[L] = dict(a=a, b=b, rms=rms, n=ne)
        m = B.pd_to_xy(L)
        m2 = B.pd_to_xy(L, channel="pd2")
        rows = []
        for t in tr:
            s = (m["track"] == t["track"]) & m["lasing"]
            v1, v2 = m["value_V"][s], m2["value_V"][s]
            rows.append((float(v1.mean()), float(v1.std()), float(v1.max()), float(v2.mean()), float((v2 / v1).mean())) if s.any() else (np.nan,) * 5)
        feats[L] = rows
        las = m["lasing"]
        med = np.median(m["value_V"][las])
        k = np.clip(np.searchsorted(tr["t_start_us"], m["t_us"], side="right") - 1, 0, None)
        settled = (m["t_us"] - tr["t_start_us"][k]) > 400.0      # skip track starts, which are bright because the spot is slow
        hot = las & settled & (m["value_V"] > 1.5 * med)
        if hot.sum() > 5:
            events.append(dict(t_utc_ns=int(g.attrs["t0_pi_ns"]), layer=int(g.attrs["layer"]), t_us=float(m["t_us"][hot].mean()),
                               source="monitor", kind="anomaly", severity=1, x_mm=float(m["x_mm"][hot].mean()), y_mm=float(m["y_mm"][hot].mean()),
                               message=f"pd1 above 1.5 x the layer median in {int(hot.sum())} samples"))
        tc = g["coax_cam/t_mid_us"][...]
        r = g["rtc"]
        t_cmd = np.arange(r["x_mm"].shape[0]) * TICK
        xc, yc = lh.model_xy(t_cmd, r["x_mm"][...], r["y_mm"][...], tc, CAL["tracking_delay_us"], "lag1")
        feats[L + "_coax"] = (xc, yc)
    B.f.close()
    with h5py.File(path, "r+") as f:
        for L, fit in fits.items():
            f[f"/layers/{L}/daq"].attrs.update(clock_a_us=fit["a"], clock_b=fit["b"], clock_fit_rms_us=fit["rms"], clock_fit_edges=fit["n"])
            ds = f[f"/layers/{L}/tracks"]
            arr = ds[...]
            for i, (m1, s1, x1, m2, rt) in enumerate(feats[L]):
                arr[i]["pd1_mean"], arr[i]["pd1_std"], arr[i]["pd1_max"], arr[i]["pd2_mean"], arr[i]["ratio_mean"] = m1, s1, x1, m2, rt
            c = f[f"/layers/{L}/coax_cam"]
            ti = c["track"][...]
            for i in range(len(arr)):
                arr[i]["coax_frames"] = int((ti == arr[i]["track"]).sum())
            ds[...] = arr
            lh.put(c["x_mm"], feats[L + "_coax"][0]); lh.put(c["y_mm"], feats[L + "_coax"][1])
        lh.append(f["/events"], events)
    return fits


def check(path, truths, fits):
    """Reader vs truth on layer 2: position error of every lasing sample, four ways; hot-spot location; the figure."""
    B = lh.Build(path)
    L = "L00002"
    truth, tracks, on, off = truths[2]
    variants = {"first edge only, nominal rate, no tracking delay": dict(use_fit=False, use_tau=False),
                "clock fit, no tracking delay": dict(use_tau=False),
                "clock fit + pure 250 µs delay": dict(model="delay"),
                "clock fit + first-order lag (250 µs)": dict(model="lag1")}
    t_true = truth["ts"] - CAL["pd_delay_us"]                   # emission time of each sample, on the RTC6 clock
    xt, yt = np.interp(t_true, truth["tf"], truth["xa"]), np.interp(t_true, truth["tf"], truth["ya"])
    res, maps = {}, {}
    starts = np.array([t["t_start_us"] for t in tracks])
    ends = np.array([t["t_end_us"] for t in tracks])
    for name, kw in variants.items():
        m = B.pd_to_xy(L, **kw)
        e = np.hypot(m["x_mm"] - xt, m["y_mm"] - yt) * 1e3
        las = m["lasing"]
        k = np.clip(np.searchsorted(starts, t_true, side="right") - 1, 0, None)
        since = t_true - starts[k]
        steady = las & (since > 1000.0) & (t_true < ends[k])     # at speed, before the command stops
        v = m["value_V"]
        hot = las & (since > 400.0) & (v > 1.5 * np.median(v[las]))
        hx, hy = m["x_mm"][hot], m["y_mm"][hot]
        axis = 1                                                 # layer 2 hatches along y, so the lag spreads the spot along y
        res[name] = dict(median_um=round(float(np.median(e[las])), 1), p95_um=round(float(np.percentile(e[las], 95)), 1),
                         steady_median_um=round(float(np.median(e[steady])), 1), steady_p95_um=round(float(np.percentile(e[steady], 95)), 1),
                         hot_centroid_mm=[round(float(hx.mean()), 3), round(float(hy.mean()), 3)],
                         hot_centroid_error_um=round(float(np.hypot(hx.mean() - DEFECT["x"], hy.mean() - DEFECT["y"]) * 1e3), 1),
                         hot_spread_along_scan_um=round(float(np.std(hy if axis else hx) * 1e3), 1), n_hot=int(hot.sum()))
        maps[name] = (m, e, since, las)
    a_true = DAQ_LEAD * -1                                      # sample 0 at t0 - lead
    fit = fits[L]
    clock = dict(a_fit_us=round(fit["a"], 3), a_true_us=round(a_true, 3), b_fit_minus_1_ppm=round((fit["b"] - 1) * 1e6, 2),
                 b_true_minus_1_ppm=round((1 / (1 + DRIFT) - 1) * 1e6, 2), rms_us=round(fit["rms"], 3), edges=fit["n"])
    drop = B.frames_check("L00003", CAM["period"])
    B.f.close()
    out = dict(layer=2, clock_fit=clock, variants=res, dropped_frames_layer3=drop.tolist(),
               defect_truth_mm=[DEFECT["x"], DEFECT["y"]], file_bytes=path.stat().st_size)
    (OUT / "reader_check.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    md = ["# Reader check on the synthetic build (generated by synthetic_build.py)", "",
          f"Layer 2, every photodiode sample taken while lasing; truth from the simulation. File: `synthetic_build.h5`, "
          f"{path.stat().st_size / 1e6:.2f} MB.", "",
          f"**Clock fit** (gate edges, {clock['edges']} used): offset {clock['a_fit_us']} µs (true {clock['a_true_us']}), "
          f"rate {clock['b_fit_minus_1_ppm']} ppm (true {clock['b_true_minus_1_ppm']}), residual RMS {clock['rms_us']} µs.", "",
          "| mapping | median error (µm) | 95th pct (µm) | steady part of tracks: median / 95th (µm) | hot spot found at (mm) | off by (µm) | spread along the scan (µm) |",
          "|---|---:|---:|---|---|---:|---:|"]
    for k, r in res.items():
        md.append(f"| {k} | {r['median_um']} | {r['p95_um']} | {r['steady_median_um']} / {r['steady_p95_um']} | "
                  f"({r['hot_centroid_mm'][0]}, {r['hot_centroid_mm'][1]}) | {r['hot_centroid_error_um']} | {r['hot_spread_along_scan_um']} |")
    md += ["", f"Planted hot spot at ({DEFECT['x']}, {DEFECT['y']}) mm. Steady = more than 1 ms after the mark command started.",
           f"Dropped frames found in layer 3 (trigger index with no frame): {drop.tolist()} (one was dropped on purpose)."]
    (OUT / "reader_check.md").write_text("\n".join(md) + "\n")
    figure(maps, truth, tracks)
    return out


def figure(maps, truth, tracks):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    ink, ink2, grid = "#191919", "#666666", "#e6e6e6"
    seq = LinearSegmentedColormap.from_list("blue", ["#cce3fd", "#84b9f3", "#338ced", "#1b64be", "#0e3d7e"])
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.4), dpi=130, gridspec_kw=dict(width_ratios=[1, 1, 1.25]))
    names = ["clock fit, no tracking delay", "clock fit + first-order lag (250 µs)"]
    titles = ["a. Clock fitted, scan-head lag ignored", "b. Clock fitted, lag corrected"]
    vmax = 0
    for name in names:
        m, _, _, las = maps[name]
        vmax = max(vmax, np.percentile(m["value_V"][las], 99.5))
    for a_, name, ttl in zip(ax[:2], names, titles):
        m, _, _, las = maps[name]
        s = las & (np.abs(m["x_mm"] - DEFECT["x"]) < 0.6) & (np.abs(m["y_mm"] - DEFECT["y"]) < 0.6)
        sc = a_.scatter(m["x_mm"][s], m["y_mm"][s], c=m["value_V"][s], s=5, cmap=seq, vmin=1.6, vmax=vmax, linewidths=0)
        a_.add_patch(plt.Circle((DEFECT["x"], DEFECT["y"]), 2 * DEFECT["r"], fill=False, ec=ink, lw=1.2))
        a_.set_title(ttl, loc="left", fontsize=10, color=ink)
        a_.set_xlim(DEFECT["x"] - 0.6, DEFECT["x"] + 0.6); a_.set_ylim(DEFECT["y"] - 0.6, DEFECT["y"] + 0.6)
        a_.set_aspect("equal"); a_.set_xlabel("x (mm)", color=ink2); a_.set_ylabel("y (mm)", color=ink2)
    ax[0].annotate("true hot spot", (DEFECT["x"] + 0.1, DEFECT["y"] + 0.1), (DEFECT["x"] + 0.15, DEFECT["y"] + 0.42), color=ink, fontsize=8,
                   arrowprops=dict(arrowstyle="-", color=ink2, lw=0.8))
    ax[0].text(DEFECT["x"] - 0.57, DEFECT["y"] - 0.56, "tracks run ±y, so one spot\nmaps to two, 0.5 mm apart", fontsize=8, color=ink2)
    cb = fig.colorbar(sc, ax=ax[:2], shrink=0.8, pad=0.02)
    cb.set_label("photodiode 1 (V)", color=ink2)
    # c: error vs time since the mark started
    bins = np.arange(0, 2050, 50.0)
    for name, col, lab in [("clock fit + pure 250 µs delay", "#f47230", "pure delay"), ("clock fit + first-order lag (250 µs)", "#257de0", "first-order lag")]:
        m, e, since, las = maps[name]
        k = np.digitize(since[las], bins) - 1
        med = np.array([np.median(e[las][k == i]) if (k == i).sum() > 5 else np.nan for i in range(len(bins) - 1)])
        ax[2].plot(bins[:-1] + 25, med, color=col, lw=2, label=lab)
        j = np.nanargmax(med)
        ax[2].text(bins[j] + 60, med[j], lab, color=ink, fontsize=8, va="bottom")
    ax[2].set_yscale("log"); ax[2].set_ylim(0.3, 300)
    ax[2].set_xlabel("time since the mark command started (µs)", color=ink2); ax[2].set_ylabel("position error, median (µm)", color=ink2)
    ax[2].set_title("c. Error along a 2 mm track at 1 m/s\n(truth: a second-order head lagging 250 µs)", loc="left", fontsize=10, color=ink)
    ax[2].legend(frameon=False, fontsize=8, loc="upper right")
    ax[2].grid(True, color=grid, lw=0.6); ax[2].set_axisbelow(True)
    for a_ in ax:
        for sp in ("top", "right"):
            a_.spines[sp].set_visible(False)
        a_.tick_params(colors=ink2, labelsize=8)
    fig.savefig(OUT / "reader_check.png", bbox_inches="tight")
    plt.close(fig)


def tree(path):
    L = ["# synthetic_build.h5: what is in it (generated by synthetic_build.py)", "", "| path | kind | shape | dtype |", "|---|---|---|---|"]
    with h5py.File(path, "r") as f:
        def v(n, o):
            if isinstance(o, h5py.Dataset):
                L.append(f"| `/{n}` | {'table' if o.dtype.names else 'array'} | {o.shape} | {'compound (' + str(len(o.dtype.names)) + ' fields)' if o.dtype.names else o.dtype} |")
            else:
                L.append(f"| `/{n}` | group, {len(o.attrs)} attrs | | |")
        f.visititems(v)
    (OUT / "synthetic_tree.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    path, truths = write()
    fits = postprocess(path, truths)
    out = check(path, truths, fits)
    tree(path)
    lh.export_nist_style(path, Path("/tmp/nist_style_export"))
    print(json.dumps(out, indent=1, ensure_ascii=False))
