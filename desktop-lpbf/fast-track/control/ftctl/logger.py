"""Build log on one time base: events as JSON lines while the build runs (survive a crash), and at the end one HDF5
file with samples, layers, events and markers, plus a summary JSON.

HDF5 layout (all times in seconds on the supervisor's clock, t = 0 when the supervisor started):
  /samples   compound: t, state, plate_C, block_C, plate_out_pct, block_out_pct, o2_ppm, room_o2_pct, box_air_C,
             window_C, beam_tube_C, stage_C, piston_mm, recoater_mm, safety_ok, laser_ps, laser_emission, limit_ok,
             k1_on, argon, vibrator
  /layers    compound: one row per layer (planned and measured times, energy, temperatures, O2, completion)
  /events    compound: t, kind, code, text
  /markers   compound: t, layer, edge (the RTC5's DIGITAL OUT1 layer marker: 1 at list start, 0 at list end)
  attrs      config (JSON), program (path and meta JSON), time_base, ftctl version
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, List

import numpy as np

from . import __version__

SAMPLE_FIELDS = ["t", "state", "plate_C", "block_C", "plate_out_pct", "block_out_pct", "o2_ppm", "o2_pct",
                 "room_o2_pct",
                 "box_air_C", "window_C", "beam_tube_C", "stage_C", "piston_mm", "recoater_mm", "safety_ok",
                 "laser_ps", "laser_emission", "limit_ok", "k1_on", "argon", "vibrator"]
LAYER_FIELDS = ["layer", "z_mm", "t_start", "t_recoat_end", "t_scan_start", "t_scan_end", "t_end", "recoat_s",
                "scan_s", "planned_scan_s", "dwell_s", "hold_s", "energy_J", "n_vectors", "plate_C_scan_start",
                "plate_C_scan_end", "o2_ppm_scan_start", "complete"]
TIME_BASE = ("seconds since the supervisor started, from the PC's monotonic clock (RealClock) or the simulation "
             "(SimClock); the RTC5 raises DIGITAL OUT1 (LASER connector pin 12) for each layer's list, recorded "
             "with LASERON (pin 2) by the fast recorder, which ties its own sample clock to this time base")


class BuildLog:
    def __init__(self, out_dir, clock, name: str = "build"):
        self.dir = pathlib.Path(out_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.clock = clock
        self.name = name
        self.samples: List[dict] = []
        self.layers: List[dict] = []
        self.events: List[dict] = []
        self.markers: List[tuple] = []
        self.attrs: Dict[str, str] = {"time_base": TIME_BASE, "ftctl_version": __version__}
        self._jsonl = (self.dir / f"{name}-events.jsonl").open("w")

    def event(self, kind: str, code: str = "", text: str = "", **data) -> None:
        e = dict(t=self.clock.now(), kind=kind, code=code, text=text)
        if data:
            e["data"] = data
        self.events.append(e)
        self._jsonl.write(json.dumps(e, default=str) + "\n")
        self._jsonl.flush()

    def sample(self, row: dict) -> None:
        self.samples.append(row)

    def layer(self, row: dict) -> None:
        self.layers.append(row)

    def close(self, summary: dict) -> dict:
        self._jsonl.close()
        paths = dict(events_jsonl=str(self.dir / f"{self.name}-events.jsonl"))
        h5 = self.dir / f"{self.name}.h5"
        try:
            import h5py
        except ImportError:                        # pragma: no cover
            h5py = None
        if h5py is not None:
            with h5py.File(h5, "w") as f:
                for k, v in self.attrs.items():
                    f.attrs[k] = v
                f.create_dataset("samples", data=_table(self.samples, SAMPLE_FIELDS, {"state": "S16"}))
                f.create_dataset("layers", data=_table(self.layers, LAYER_FIELDS, {}))
                ev = np.array([(e["t"], e["kind"], e["code"], e["text"]) for e in self.events],
                              dtype=[("t", "f8"), ("kind", h5py.string_dtype()), ("code", h5py.string_dtype()),
                                     ("text", h5py.string_dtype())])
                f.create_dataset("events", data=ev)
                mk = np.array(self.markers, dtype=[("t", "f8"), ("layer", "i4"), ("edge", "i1")])
                f.create_dataset("markers", data=mk)
                f.attrs["summary"] = json.dumps(summary, default=str)
            paths["hdf5"] = str(h5)
        sp = self.dir / f"{self.name}-summary.json"
        summary = dict(summary, files=paths)
        sp.write_text(json.dumps(summary, indent=1, default=_json_default))
        summary["files"]["summary"] = str(sp)
        return summary


def _json_default(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    return str(o)


def _table(rows, fields, special):
    dt = [(k, special.get(k, "f8")) for k in fields]
    arr = np.zeros(len(rows), dtype=dt)
    for i, r in enumerate(rows):
        for k in fields:
            v = r.get(k, math.nan if special.get(k, "f8") == "f8" else "")
            if special.get(k) and isinstance(v, str):
                v = v.encode()[:16]
            arr[i][k] = v if v is not None else math.nan
    return arr


def read_h5(path) -> dict:
    """Load a build log back into numpy arrays (for plots and tests)."""
    import h5py
    with h5py.File(path, "r") as f:
        return dict(samples=f["samples"][()], layers=f["layers"][()], events=f["events"][()],
                    markers=f["markers"][()], attrs={k: f.attrs[k] for k in f.attrs})
