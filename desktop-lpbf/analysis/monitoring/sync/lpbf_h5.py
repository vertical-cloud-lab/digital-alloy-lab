#!/usr/bin/env python3
"""One HDF5 file per build for the desktop LPBF's monitoring data: the schema, a writer, and a reader (issue #260,
monitoring/sync-and-data.md §4).

The schema is data (SPEC below), so the empty file, the field table in schema.md and the writer all come from one place.
Times: the RTC6's 10 µs clock is the master. Inside a layer every fast time is "µs since the layer's t0_tick" on that clock.
The digitizer runs on its own crystal and is mapped onto the RTC6 clock by fitting its recorded laser-gate edges to the gate
edges the job commanded (fit_clock). The beam position comes from the commanded log, shifted by the scan head's lag
(model_xy: "lag1" = first-order lag with time constant tau, which has exactly tau of lag at constant speed, SCANLAB's
definition of tracking error; "delay" = pure delay tau).

    python desktop-lpbf/analysis/monitoring/sync/lpbf_h5.py      # writes schema_empty.h5 and schema.md
"""
from __future__ import annotations

import json
from pathlib import Path

import h5py
import numpy as np

SCHEMA_NAME, SCHEMA_VERSION = "desktop-lpbf-monitoring", "0.1.0"
STR = h5py.string_dtype()
HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "out" / "monitoring" / "sync"

# --------------------------------------------------------------------------------------------------------------- the spec
# kind: group (attrs), table (compound dataset, fields), array (N-d dataset). Paths with {L} are made once per layer.
# attrs / fields: (name, dtype, units, description). dtype "str" = variable-length UTF-8.
SPEC = [
    dict(path="/", kind="group", desc="one build", attrs=[
        ("schema", "str", "", f"'{SCHEMA_NAME}'"), ("schema_version", "str", "", "semantic version of this layout"),
        ("build_id", "str", "", "unique build id, also the file name"), ("created_utc", "str", "ISO 8601", "file creation"),
        ("writer", "str", "", "program and git commit that wrote the file")]),
    dict(path="/build", kind="group", desc="per-build metadata (monitoring.md §5.2)", attrs=[
        ("start_utc", "str", "ISO 8601", "first layer's t0"), ("end_utc", "str", "ISO 8601", "last layer's scan end"),
        ("run_by", "str", "", "person, or robot job id"), ("recipe", "str", "", "recipe name"),
        ("recipe_sha256", "str", "", "hash of the recipe file"), ("scan_file", "str", "", "job / scan file name"),
        ("scan_file_sha256", "str", "", "hash of the scan file"), ("alloy", "str", "", "e.g. AlSi10Mg, 6061+Zr"),
        ("powder_lot", "str", "", "lot id read from the reservoir's NFC tag (P-05)"), ("plate_id", "str", "", "plate serial"),
        ("plate_material", "str", "", ""), ("module", "str", "", "S25, M50 or L75"), ("module_id", "str", "", "module serial"),
        ("layer_um", "f8", "µm", "nominal layer thickness"), ("n_layers", "i4", "", "layers built"),
        ("plate_setpoint_C", "f8", "°C", "preheat set point"), ("focus_offset_mm", "f8", "mm", "z offset of focus from the powder surface"),
        ("spot_um", "f8", "µm", "1/e² spot diameter at focus"),
        ("field_correction", "str", "", "RTC6 correction file (.ct5) name"), ("field_correction_sha256", "str", "", ""),
        ("cover_slide_count", "i4", "", "builds on this cover slide"), ("start_O2_ppm", "f8", "ppm", "at the first layer"),
        ("start_dewpoint_C", "f8", "°C", "at the first layer"), ("power_check_W", "f8", "W", "power-head reading before the build"),
        ("software_commit", "str", "", "git commit of the control software"), ("rtc6_software", "str", "", "RTC6 DLL / firmware versions"),
        ("monitoring_config", "str", "JSON", "instrument settings: gains, ranges, frame rates, filters")]),
    dict(path="/build/parts", kind="table", desc="parts on the plate", fields=[
        ("part", "i4", "", "part id"), ("name", "str", "", ""), ("x_mm", "f4", "mm", "centroid x, plate frame"),
        ("y_mm", "f4", "mm", "centroid y"), ("rot_deg", "f4", "deg", ""), ("param_set", "i2", "", "default parameter set"),
        ("stl_sha256", "str", "", "")]),
    dict(path="/build/param_sets", kind="table", desc="laser and scanner parameters (all RTC6 delays, so gate edges can be predicted)", fields=[
        ("id", "i2", "", ""), ("name", "str", "", ""), ("power_W", "f4", "W", ""), ("speed_mm_s", "f4", "mm/s", "mark speed"),
        ("jump_speed_mm_s", "f4", "mm/s", ""), ("hatch_um", "f4", "µm", ""), ("layer_um", "f4", "µm", ""),
        ("laser_on_delay_us", "f4", "µs", "LASERON after the mark starts"), ("laser_off_delay_us", "f4", "µs", "LASERON off after the mark ends"),
        ("mark_delay_us", "f4", "µs", ""), ("jump_delay_us", "f4", "µs", ""), ("polygon_delay_us", "f4", "µs", ""),
        ("skywriting", "u1", "", "0/1"), ("strategy", "str", "", "e.g. serpentine, 67° rotation")]),
    dict(path="/clocks", kind="table", desc="clock domains and how they are tied to the RTC6", fields=[
        ("name", "str", "", ""), ("unit", "str", "", ""), ("nominal_Hz", "f8", "Hz", ""), ("tied_by", "str", "", "")]),
    dict(path="/calibration/timing", kind="group", desc="delays measured by the calibration routine (sync-and-data.md §1.5)", attrs=[
        ("tracking_delay_us", "f8", "µs", "scan head lag at constant speed"), ("tracking_delay_unc_us", "f8", "µs", ""),
        ("galvo_model", "str", "", "'lag1' or 'delay'"), ("laser_rise_us", "f8", "µs", "gate edge to light"),
        ("pd_delay_us", "f8", "µs", "photodiode + cable group delay"), ("gate_tap_delay_us", "f8", "µs", "RC of the gate tap"),
        ("ae_path_delay_us", "f8", "µs", "melt pool to AE sensor"), ("coax_trigger_to_exposure_us", "f8", "µs", "XTR edge to exposure start"),
        ("coax_trigger_jitter_us", "f8", "µs", ""), ("chronos_trigger_to_exposure_us", "f8", "µs", ""),
        ("gen_latency_us", "f8", "µs", "window edge to first trigger"), ("method", "str", "", ""), ("date_utc", "str", "ISO 8601", "")]),
    dict(path="/calibration/geometry", kind="group", desc="spatial registration", attrs=[
        ("rtc_bits_per_mm", "f8", "bit/mm", "RTC6 calibration factor K"), ("coax_um_per_px", "f8", "µm/px", ""),
        ("coax_spot_px", "f8", "px", "laser spot centre in the coaxial image (x, y)"), ("coax_rotation_deg", "f8", "deg", "image to plate"),
        ("plate_from_rtc", "f8", "", "2 x 3 affine, RTC mm to plate mm"), ("layer_cam_homography", "f8", "", "3 x 3, plate mm to pixels"),
        ("side_cam_homography", "f8", "", "3 x 3, plate mm to pixels"), ("date_utc", "str", "ISO 8601", "")]),
    dict(path="/calibration/geometry/spot_grid", kind="table", desc="pulsed-spot grid: commanded vs seen", fields=[
        ("instrument", "str", "", "coax_cam, layer_cam, side_cam, pd1"), ("x_cmd_mm", "f4", "mm", ""), ("y_cmd_mm", "f4", "mm", ""),
        ("u_px", "f4", "px", "seen (or 0 for a photodiode)"), ("v_px", "f4", "px", ""), ("signal", "f4", "", "peak signal")]),
    dict(path="/calibration/radiometry", kind="group", desc="photodiode bands, gains, dark levels", attrs=[
        ("pd1_band_nm", "f8", "nm", "centre, FWHM"), ("pd2_band_nm", "f8", "nm", ""), ("pd1_gain_dB", "f8", "dB", ""),
        ("pd2_gain_dB", "f8", "dB", ""), ("pd1_dark_V", "f8", "V", ""), ("pd2_dark_V", "f8", "V", ""),
        ("lamp", "str", "", "ratio calibration source (Hooper 2018 style)")]),
    dict(path="/calibration/ae", kind="group", desc="AE chain and the pencil-lead breaks before the build", attrs=[
        ("sensor", "str", "", ""), ("preamp", "str", "", ""), ("gain_dB", "f8", "dB", ""), ("filter_kHz", "f8", "kHz", "band-pass"),
        ("threshold_dBAE", "f8", "dBAE", ""), ("couplant", "str", "", ""), ("preload_N", "f8", "N", "")]),
    dict(path="/calibration/ae/plb", kind="table", desc="Hsu-Nielsen breaks", fields=[
        ("x_mm", "f4", "mm", ""), ("y_mm", "f4", "mm", ""), ("amplitude_dBAE", "f4", "dBAE", ""), ("t_utc_ns", "i8", "ns", "")]),
    dict(path="/layers/{L}", kind="group", desc="one layer", attrs=[
        ("layer", "i4", "", "1-based"), ("z_mm", "f8", "mm", "build height at this layer"),
        ("t0_tick", "u8", "10 µs", "RTC6 tick at the layer start; all layer times are µs after it"),
        ("t0_utc", "str", "ISO 8601", "from t0_pi_ns"), ("t0_pi_ns", "u8", "ns", "Pi kernel timestamp of the layer-start bit"),
        ("scan_end_us", "f8", "µs", "end of the last vector"), ("recoat_start_utc", "str", "ISO 8601", ""), ("recoat_end_utc", "str", "ISO 8601", ""),
        ("dwell_s", "f4", "s", "hold for plate temperature"), ("plate_T_start_C", "f4", "°C", ""), ("n_tracks", "i4", "", ""),
        ("hatch_angle_deg", "f4", "deg", "")]),
    dict(path="/layers/{L}/rtc", kind="group", desc="RTC6 log: one row per 10 µs tick (NIST's XYPT, plus the output word)", attrs=[
        ("period_us", "f8", "µs", "10"), ("source", "str", "", "set_trigger4 or StreamParser"), ("signals", "str", "", "RTC6 signal names")]),
    dict(path="/layers/{L}/rtc/x_mm", kind="array", dtype="f4", ndim=1, units="mm", desc="commanded x (SampleX / K)"),
    dict(path="/layers/{L}/rtc/y_mm", kind="array", dtype="f4", ndim=1, units="mm", desc="commanded y"),
    dict(path="/layers/{L}/rtc/power_W", kind="array", dtype="f4", ndim=1, units="W", desc="commanded power (ANALOG OUT1 scaled)"),
    dict(path="/layers/{L}/rtc/laser_on", kind="array", dtype="u1", ndim=1, units="", desc="LASERON at the tick"),
    dict(path="/layers/{L}/rtc/dout", kind="array", dtype="u2", ndim=1, units="", desc="16-bit digital output word (bit 0 camera window, 1 layer start, 2 track toggle, 3 Chronos record end)"),
    dict(path="/layers/{L}/tracks", kind="table", desc="one row per mark (track), with features filled in after the layer", fields=[
        ("track", "i4", "", ""), ("part", "i4", "", ""), ("kind", "i1", "", "0 hatch, 1 contour, 2 support, 3 calibration"),
        ("param_set", "i2", "", ""), ("t_start_us", "f8", "µs", "mark command starts"), ("t_end_us", "f8", "µs", "mark command ends"),
        ("x0_mm", "f4", "mm", ""), ("y0_mm", "f4", "mm", ""), ("x1_mm", "f4", "mm", ""), ("y1_mm", "f4", "mm", ""),
        ("speed_mm_s", "f4", "mm/s", ""), ("power_W", "f4", "W", ""), ("camera", "u1", "", "camera window set"),
        ("pd1_mean", "f4", "V", ""), ("pd1_std", "f4", "V", ""), ("pd1_max", "f4", "V", ""), ("pd2_mean", "f4", "V", ""),
        ("ratio_mean", "f4", "", "pd2/pd1"), ("coax_frames", "i4", "", ""), ("coax_area_px", "f4", "px", "mean pool area"),
        ("ae_hits", "i4", "", ""), ("flag", "i1", "", "0 ok, 1 anomaly")]),
    dict(path="/layers/{L}/daq", kind="group", desc="digitizer stream for the layer, mapped to the RTC6 clock by fit_clock", attrs=[
        ("fs_Hz", "f8", "Hz", "nominal sample rate"), ("t0_index", "i8", "", "index of the first sample in the stream"),
        ("clock_a_us", "f8", "µs", "t_rtc = a + b * (index / fs) * 1e6"), ("clock_b", "f8", "", "rate ratio, 1 + drift"),
        ("clock_fit_rms_us", "f8", "µs", ""), ("clock_fit_edges", "i4", "", "gate edges used"), ("instrument", "str", "", "")]),
    dict(path="/layers/{L}/daq/pd1", kind="array", dtype="i2", ndim=1, units="count", desc="photodiode 1 (ch A); attrs volts_per_count, offset_V"),
    dict(path="/layers/{L}/daq/pd2", kind="array", dtype="i2", ndim=1, units="count", desc="photodiode 2 (ch B)"),
    dict(path="/layers/{L}/daq/ae", kind="array", dtype="i2", ndim=1, units="count", desc="AE from the decoupler (ch C)"),
    dict(path="/layers/{L}/daq/gate", kind="array", dtype="i2", ndim=1, units="count", desc="laser gate tap (ch D): the sync reference"),
    dict(path="/layers/{L}/ae_hits", kind="table", desc="AE hits from the layer start to the next layer start", fields=[
        ("t_us", "f8", "µs", "RTC6 time after t0 (corrected for ae_path_delay)"), ("peak_V", "f4", "V", ""), ("amplitude_dBAE", "f4", "dBAE", ""),
        ("energy_V2s", "f4", "V² s", ""), ("rise_us", "f4", "µs", ""), ("duration_us", "f4", "µs", ""), ("counts", "i4", "", ""),
        ("rms_V", "f4", "V", ""), ("skewness", "f4", "", ""), ("kurtosis", "f4", "", ""), ("snippet", "i4", "", "row in ae_snippets, -1 none"),
        ("label", "i1", "", "-1 unknown, 0 noise, 1 crack-like")]),
    dict(path="/layers/{L}/ae_snippets", kind="array", dtype="i2", ndim=2, units="count", desc="raw AE around each hit (rows); attrs fs_Hz, pre_samples, volts_per_count"),
    dict(path="/layers/{L}/coax_cam", kind="group", desc="coaxial camera, one frame per trigger", attrs=[
        ("sensor", "str", "", ""), ("roi", "i4", "px", "x, y, w, h"), ("band_nm", "f8", "nm", "centre, FWHM"), ("analogue_gain", "f8", "", ""),
        ("trigger_period_us", "f8", "µs", ""), ("trigger_delay_us", "f8", "µs", "first trigger after the window edge")]),
    dict(path="/layers/{L}/coax_cam/frames", kind="array", dtype="u2", ndim=3, units="DN", desc="frames, one per row"),
    dict(path="/layers/{L}/coax_cam/t_mid_us", kind="array", dtype="f8", ndim=1, units="µs", desc="mid-exposure, RTC6 time after t0"),
    dict(path="/layers/{L}/coax_cam/exposure_us", kind="array", dtype="f4", ndim=1, units="µs", desc="low pulse + 14.26 µs"),
    dict(path="/layers/{L}/coax_cam/trigger_index", kind="array", dtype="i4", ndim=1, units="", desc="which trigger of the layer made it"),
    dict(path="/layers/{L}/coax_cam/pi_ts_ns", kind="array", dtype="u8", ndim=1, units="ns", desc="libcamera SensorTimestamp (drop check only)"),
    dict(path="/layers/{L}/coax_cam/track", kind="array", dtype="i4", ndim=1, units="", desc="track at mid-exposure"),
    dict(path="/layers/{L}/coax_cam/x_mm", kind="array", dtype="f4", ndim=1, units="mm", desc="beam x at mid-exposure (reader)"),
    dict(path="/layers/{L}/coax_cam/y_mm", kind="array", dtype="f4", ndim=1, units="mm", desc="beam y at mid-exposure (reader)"),
    dict(path="/layers/{L}/side_cam", kind="table", desc="Chronos bursts (frames stay in external files)", fields=[
        ("segment", "i2", "", ""), ("file", "str", "", "relative path"), ("sha256", "str", "", ""), ("n_frames", "i4", "", ""),
        ("t_first_us", "f8", "µs", "first frame, RTC6 time after t0"), ("period_us", "f8", "µs", ""), ("exposure_us", "f4", "µs", ""),
        ("roi", "str", "", ""), ("mode", "str", "", "exposure trigger / shutter gating")]),
    dict(path="/layers/{L}/layer_images", kind="group", desc="layer camera stills: datasets '<stage>_<light>' (after_spread_raking, after_lasing_steep, ...)", attrs=[
        ("camera", "str", "", ""), ("lens", "str", "", ""), ("f_number", "f8", "", "")]),
    dict(path="/layers/{L}/layer_images/after_spread_raking", kind="array", dtype="u2", ndim=2, units="DN",
         desc="one still; attrs stage, light, exposure_us, analogue_gain, sensor_temp_C, t_utc"),
    dict(path="/slow", kind="table", desc="PLC channels over Modbus TCP, time-stamped on the Pi (electrical-io.csv ids)", fields=[
        ("t_utc_ns", "i8", "ns", ""), ("layer", "i4", "", "current layer, 0 before the first"), ("plate_T_C", "f4", "°C", "H-02"),
        ("edge_T_C", "f4", "°C", "H-03"), ("wall_T_C", "f4", "°C", "P-09"), ("cake_T_C", "f4", "°C", "P-10"), ("heater_duty", "f4", "", "H-01"),
        ("O2_ppm", "f4", "ppm", "G-01"), ("dewpoint_C", "f4", "°C", "G-02"), ("p_abs_mbar", "f4", "mbar", "G-03"), ("dp_mbar", "f4", "mbar", "G-04"),
        ("pirani_mbar", "f4", "mbar", "G-06"), ("blower_pct", "f4", "%", "G-14"), ("recoater_mm", "f4", "mm", "M-01"),
        ("recoater_torque_pct", "f4", "%", "M-01 HLFB"), ("z_mm", "f4", "mm", "M-02"), ("door_closed", "u1", "", "M-08"),
        ("drawer_closed", "u1", "", "P-03"), ("laser_ready", "u1", "", "L-07"), ("emission_on", "u1", "", "L-07")]),
    dict(path="/ae_cooldown", kind="table", desc="AE hits after the last layer (>= 1 h)", fields=[
        ("t_utc_ns", "i8", "ns", ""), ("peak_V", "f4", "V", ""), ("amplitude_dBAE", "f4", "dBAE", ""), ("energy_V2s", "f4", "V² s", ""),
        ("plate_T_C", "f4", "°C", "at the hit"), ("label", "i1", "", "-1 unknown, 0 noise, 1 crack-like")]),
    dict(path="/events", kind="table", desc="anomalies, holds, stops, operator notes", fields=[
        ("t_utc_ns", "i8", "ns", ""), ("layer", "i4", "", ""), ("t_us", "f8", "µs", "RTC6 time after the layer's t0, NaN if none"),
        ("source", "str", "", "monitor, plc, rtc6, operator"), ("kind", "str", "", "anomaly, hold, stop, note, fault"),
        ("severity", "i1", "", "0 note, 1 flag, 2 hold at next layer, 3 stop now"), ("x_mm", "f4", "mm", ""), ("y_mm", "f4", "mm", ""),
        ("message", "str", "", "")]),
]

CLOCKS = [("rtc6", "tick (10 µs)", 1e5, "master"),
          ("daq", "sample", 2e6, "per-layer linear fit of recorded gate edges to commanded ones (fit_clock)"),
          ("pi", "ns, CLOCK_REALTIME (chrony to the lab's time server)", 1e9, "layer-start bit time-stamped on a Pi GPIO"),
          ("chronos", "µs, camera clock", 1e6, "frames counted back from the record-end trigger; TRIG1 exposure trigger"),
          ("utc", "ns", 1e9, "through the Pi")]


def _np(dt):
    return STR if dt == "str" else np.dtype(dt)


def _default(dt):
    return "" if dt == "str" else (np.nan if dt.startswith("f") else 0)


def _compound(fields):
    return np.dtype([(n, _np(d)) for n, d, _, _ in fields])


def _mk(f, node, L):
    path = node["path"].replace("{L}", L)
    if node["kind"] == "group":
        g = f.require_group(path)
        g.attrs["description"] = node["desc"]
        for n, d, u, _ in node["attrs"]:
            if n not in g.attrs:
                g.attrs[n] = _default(d) if d != "str" else ""
        g.attrs["attr_units"] = json.dumps({n: u for n, _, u, _ in node["attrs"]}, ensure_ascii=False)
        g.attrs["attr_descriptions"] = json.dumps({n: s for n, _, _, s in node["attrs"]}, ensure_ascii=False)
    elif node["kind"] == "table":
        if path in f:
            return
        ds = f.create_dataset(path, shape=(0,), maxshape=(None,), dtype=_compound(node["fields"]), chunks=True)
        ds.attrs["description"] = node["desc"]
        ds.attrs["field_units"] = json.dumps({n: u for n, _, u, _ in node["fields"]}, ensure_ascii=False)
        ds.attrs["field_descriptions"] = json.dumps({n: s for n, _, _, s in node["fields"]}, ensure_ascii=False)
    else:
        if path in f:
            return
        nd = node["ndim"]
        ds = f.create_dataset(path, shape=(0,) * nd, maxshape=(None,) * nd, dtype=node["dtype"], chunks=True,
                              compression="gzip", compression_opts=4, shuffle=True, fletcher32=True)
        ds.attrs["units"], ds.attrs["description"] = node["units"], node["desc"]


def create(path, build_id="template", writer="lpbf_h5.py", layer_template=True, created_utc=None):
    """A new build file with every non-layer node, and (for the empty schema file) the layer template '_template'."""
    f = h5py.File(path, "w", libver="latest")
    for node in SPEC:
        if "{L}" not in node["path"]:
            _mk(f, node, "")
    f.attrs.update(schema=SCHEMA_NAME, schema_version=SCHEMA_VERSION, build_id=build_id, writer=writer,
                   created_utc=created_utc or np.datetime_as_string(np.datetime64("now", "s")) + "Z")
    append(f["/clocks"], CLOCKS)
    if layer_template:
        add_layer(f, "_template")
    return f


def add_layer(f, idx):
    L = idx if isinstance(idx, str) else f"L{idx:05d}"
    for node in SPEC:
        if "{L}" in node["path"]:
            _mk(f, node, L)
    return f[f"/layers/{L}"]


def append(ds, rows):
    rows = list(rows)
    if not rows:
        return ds
    n = ds.shape[0]
    ds.resize((n + len(rows),))
    arr = np.empty(len(rows), dtype=ds.dtype)
    for i, r in enumerate(rows):
        arr[i] = tuple(r.get(k, _default(str(ds.dtype[k]))) for k in ds.dtype.names) if isinstance(r, dict) else tuple(r)
    ds[n:] = arr
    return ds


def put(ds, data, **attrs):
    """Fill an (empty, extensible) array dataset with data, and set attrs."""
    data = np.asarray(data, dtype=ds.dtype)
    ds.resize(data.shape)
    if data.size:
        ds[...] = data
    ds.attrs.update(attrs)
    return ds


# --------------------------------------------------------------------------------------------------------------- reader
def gate_edges_expected(tracks, params):
    """Commanded LASERON edges (RTC6 µs after t0) from the track table and each parameter set's laser delays."""
    p = {int(r["id"]): r for r in params}
    on = np.array([t["t_start_us"] + p[int(t["param_set"])]["laser_on_delay_us"] for t in tracks])
    off = np.array([t["t_end_us"] + p[int(t["param_set"])]["laser_off_delay_us"] for t in tracks])
    return on, off


def gate_edges_seen(gate, fs):
    """Rising and falling crossings of the gate channel at mid-level, interpolated to a fraction of a sample (seconds of DAQ time)."""
    g = gate.astype(np.float64)
    lo, hi = np.percentile(g, 1), np.percentile(g, 99)
    th = 0.5 * (lo + hi)
    s = g > th
    i = np.flatnonzero(s[1:] != s[:-1])
    frac = (th - g[i]) / (g[i + 1] - g[i])
    t = (i + frac) / fs
    rising = s[i + 1]
    return t[rising], t[~rising]


def fit_clock(seen_on, seen_off, exp_on, exp_off, tap_us=0.0, tol_us=20.0):
    """Map DAQ seconds to RTC6 µs: t_rtc = a + b * t_daq * 1e6. Seed with the first rising edge, then grow the match window by
    window, refitting, so a drift of 100 ppm over a long layer is followed. Returns a, b, rms_us, n_edges."""
    e_t = np.r_[exp_on, exp_off] + tap_us
    e_s = np.r_[np.ones(len(exp_on)), np.zeros(len(exp_off))]
    s_t = np.r_[seen_on, seen_off]
    s_s = np.r_[np.ones(len(seen_on)), np.zeros(len(seen_off))]
    oe, os_ = np.argsort(e_t), np.argsort(s_t)
    e_t, e_s, s_t, s_s = e_t[oe], e_s[oe], s_t[os_], s_s[os_]
    a, b = e_t[e_s == 1][0] - s_t[s_s == 1][0] * 1e6, 1.0
    used = None                                                   # (expected times, seen times) of the last good fit
    for n_use in (8, 32, 128, 512, len(e_t)):
        pred = (e_t[:n_use] - a) / b / 1e6                       # where each expected edge should be, in DAQ seconds
        j = np.clip(np.searchsorted(s_t, pred), 1, len(s_t) - 1)
        j = np.where(np.abs(s_t[j - 1] - pred) < np.abs(s_t[j] - pred), j - 1, j)
        ok = (np.abs(s_t[j] - pred) * 1e6 < tol_us) & (s_s[j] == e_s[:n_use])
        if ok.sum() < 2:
            continue
        A = np.c_[np.ones(ok.sum()), s_t[j[ok]] * 1e6]
        (a, b), *_ = np.linalg.lstsq(A, e_t[:n_use][ok], rcond=None)
        used = (e_t[:n_use][ok], s_t[j[ok]])
    if used is None:
        raise ValueError("fit_clock: fewer than two gate edges matched")
    res = used[0] - (a + b * used[1] * 1e6)
    return float(a), float(b), float(np.sqrt(np.mean(res ** 2))), int(len(res))


def model_xy(t_cmd_us, x_cmd, y_cmd, t_query_us, tau_us, model="lag1"):
    """Beam position at t_query from the 10 µs commanded log. 'delay': x_cmd(t - tau). 'lag1': first-order lag (time constant
    tau, zero-order-held input), which lags exactly tau at constant speed."""
    if model == "delay":
        return np.interp(t_query_us - tau_us, t_cmd_us, x_cmd), np.interp(t_query_us - tau_us, t_cmd_us, y_cmd)
    dt = float(t_cmd_us[1] - t_cmd_us[0])
    k = np.exp(-dt / tau_us)
    from scipy.signal import lfilter
    # y[n] = k y[n-1] + (1-k) x[n-1]; zi = x[0] starts it at rest on the first commanded point
    xa = lfilter([0.0, 1 - k], [1.0, -k], x_cmd, zi=[x_cmd[0]])[0]
    ya = lfilter([0.0, 1 - k], [1.0, -k], y_cmd, zi=[y_cmd[0]])[0]
    return np.interp(t_query_us, t_cmd_us, xa), np.interp(t_query_us, t_cmd_us, ya)


class Build:
    """Read a build file. pd_to_xy() is the main use: digitizer sample -> (x, y, layer, track)."""

    def __init__(self, path):
        self.f = h5py.File(path, "r")

    def layers(self):
        return sorted(k for k in self.f["/layers"] if not k.startswith("_"))

    def timing(self):
        return dict(self.f["/calibration/timing"].attrs)

    def clock(self, L, refit=False):
        d = self.f[f"/layers/{L}/daq"]
        if not refit and np.isfinite(d.attrs["clock_a_us"]):
            return d.attrs["clock_a_us"], d.attrs["clock_b"]
        tr, ps = self.f[f"/layers/{L}/tracks"][...], self.f["/build/param_sets"][...]
        eon, eoff = gate_edges_expected(tr, ps)
        son, soff = gate_edges_seen(d["gate"][...], d.attrs["fs_Hz"])
        a, b, rms, n = fit_clock(son, soff, eon, eoff, tap_us=self.timing()["gate_tap_delay_us"])
        return a, b

    def pd_to_xy(self, L, idx=None, channel="pd1", model=None, use_tau=True, use_fit=True):
        """For digitizer samples idx (default: all) of layer L: RTC6 time of emission, beam x, y, laser state, track, layer, z.
        use_tau=False / use_fit=False reproduce the uncorrected mappings the check compares against."""
        g, tm = self.f[f"/layers/{L}"], self.timing()
        d = g["daq"]
        fs = d.attrs["fs_Hz"]
        raw = d[channel][...] if idx is None else d[channel][idx]
        idx = np.arange(d[channel].shape[0]) if idx is None else np.asarray(idx)
        if use_fit:
            a, b = self.clock(L)
        else:                                   # aligned on the first gate edge only, nominal rate
            son, _ = gate_edges_seen(d["gate"][...], fs)
            eon, _ = gate_edges_expected(g["tracks"][...], self.f["/build/param_sets"][...])
            a, b = eon[0] + tm["gate_tap_delay_us"] - son[0] * 1e6, 1.0
        t_emit = a + b * (idx / fs) * 1e6 - tm["pd_delay_us"]
        r = g["rtc"]
        n = r["x_mm"].shape[0]
        t_cmd = np.arange(n) * r.attrs["period_us"]
        tau = tm["tracking_delay_us"] if use_tau else 0.0
        mdl = model or tm["galvo_model"]
        if tau > 0:
            x, y = model_xy(t_cmd, r["x_mm"][...], r["y_mm"][...], t_emit, tau, mdl)
        else:
            x, y = np.interp(t_emit, t_cmd, r["x_mm"][...]), np.interp(t_emit, t_cmd, r["y_mm"][...])
        tr = g["tracks"][...]
        tc = t_emit - tau                       # commanded time of the position the beam is at
        k = np.searchsorted(tr["t_start_us"], tc) - 1
        inside = (k >= 0) & (tc <= tr["t_end_us"][np.clip(k, 0, None)])
        track = np.where(inside, tr["track"][np.clip(k, 0, None)], -1)
        eon, eoff = gate_edges_expected(tr, self.f["/build/param_sets"][...])
        kk = np.searchsorted(eon, t_emit - tm["laser_rise_us"]) - 1
        lasing = (kk >= 0) & (t_emit - tm["laser_rise_us"] <= eoff[np.clip(kk, 0, None)])
        vpc, off = d[channel].attrs.get("volts_per_count", 1.0), d[channel].attrs.get("offset_V", 0.0)
        return dict(t_us=t_emit, x_mm=x, y_mm=y, lasing=lasing, track=track, layer=int(g.attrs["layer"]),
                    z_mm=float(g.attrs["z_mm"]), value_V=raw * vpc + off)

    def expected_triggers(self, L):
        """The generator's schedule (RTC6 µs after t0): for each track with the camera window set, a trigger at
        t_start + gen_latency + trigger_delay, then every trigger_period while the exposure still ends before t_end."""
        g, tm = self.f[f"/layers/{L}"], self.timing()
        c = g["coax_cam"]
        per, dl = c.attrs["trigger_period_us"], c.attrs["trigger_delay_us"]
        exp = float(c["exposure_us"][0]) if c["exposure_us"].shape[0] else 0.0
        out = []
        for t in g["tracks"][...]:
            if not t["camera"]:
                continue
            tt = t["t_start_us"] + tm["gen_latency_us"] + dl
            while tt + exp < t["t_end_us"]:
                out.append(tt)
                tt += per
        return np.array(out)

    def frames_check(self, L):
        """Match each frame's Pi time stamp to the trigger schedule and return the triggers that produced no frame. The offset
        between the two clocks (readout time, layer-start stamp) is the median over the first frames, which assumes the first
        five were not dropped; a frame matches a trigger within half the trigger spacing."""
        g = self.f[f"/layers/{L}"]
        trig = self.expected_triggers(L)
        pi = (g["coax_cam/pi_ts_ns"][...].astype(np.int64) - np.int64(g.attrs["t0_pi_ns"])) / 1e3      # µs after t0, Pi clock
        if not len(trig) or not len(pi):
            return np.arange(len(trig))
        off = np.median(pi[:5] - trig[:5])
        k = np.clip(np.searchsorted(trig, pi - off), 1, len(trig) - 1)
        k = np.where(np.abs(trig[k - 1] - (pi - off)) < np.abs(trig[k] - (pi - off)), k - 1, k)
        half = 0.5 * np.min(np.diff(trig)) if len(trig) > 1 else np.inf
        hit = np.abs(trig[k] - (pi - off)) < half
        return np.setdiff1d(np.arange(len(trig)), k[hit])


def export_nist_style(path, outdir):
    """Per-layer files like NIST's AMMT dataset (Lane & Yeung 2020): XYPT_L0xxx.csv (X mm, Y mm, P W, T trigger word, one row
    per 10 µs) and DAQ_L0xxx.txt (tab-separated, header with the clock fit)."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    with h5py.File(path, "r") as f:
        for L in sorted(k for k in f["/layers"] if not k.startswith("_")):
            g, n = f[f"/layers/{L}"], int(f[f"/layers/{L}"].attrs["layer"])
            r = g["rtc"]
            xypt = np.c_[r["x_mm"][...], r["y_mm"][...], r["power_W"][...], r["dout"][...]]
            np.savetxt(outdir / f"XYPT_L{n:04d}.csv", xypt, delimiter=",", fmt=["%.5f", "%.5f", "%.2f", "%d"],
                       header="X (mm),Y (mm),Power (W),Trigger", comments="")
            d = g["daq"]
            cols = [c for c in ("pd1", "pd2", "ae", "gate") if c in d]
            arr = np.c_[tuple(d[c][...] * d[c].attrs.get("volts_per_count", 1.0) for c in cols)]
            hdr = (f"desktop-lpbf DAQ export\tlayer {n}\tfs_Hz {d.attrs['fs_Hz']}\tclock_a_us {d.attrs['clock_a_us']}\t"
                   f"clock_b {d.attrs['clock_b']}\n" + "\t".join(cols) + "\n" + "\t".join(["V"] * len(cols)))
            np.savetxt(outdir / f"DAQ_L{n:04d}.txt", arr, delimiter="\t", fmt="%.5f", header=hdr, comments="")


def schema_markdown():
    L = [f"# {SCHEMA_NAME} {SCHEMA_VERSION}: every group, table and array (generated by lpbf_h5.py)", "",
         "`{L}` is one group per layer, `L00001`, `L00002`, ...; the empty schema file holds it once as `_template`. "
         "Strings are variable-length UTF-8; arrays are chunked, gzip-4 with shuffle and a Fletcher-32 checksum.", ""]
    for node in SPEC:
        L += [f"## `{node['path']}` ({node['kind']})", "", node["desc"], ""]
        if node["kind"] in ("group", "table"):
            rows = node["attrs"] if node["kind"] == "group" else node["fields"]
            L += [f"| {'attribute' if node['kind'] == 'group' else 'field'} | type | units | meaning |", "|---|---|---|---|"]
            L += [f"| `{n}` | {d} | {u} | {s} |" for n, d, u, s in rows]
        else:
            L += [f"{node['ndim']}-d `{node['dtype']}`, units {node['units'] or '-'}"]
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with create(OUT / "schema_empty.h5", build_id="empty-schema", writer="lpbf_h5.py (schema only)",
                created_utc="2026-11-25T00:00:00Z") as f:   # fixed, so a rerun gives the same file
        pass
    (OUT / "schema.md").write_text(schema_markdown())
    print("wrote", OUT / "schema_empty.h5", (OUT / "schema_empty.h5").stat().st_size, "bytes and schema.md")
